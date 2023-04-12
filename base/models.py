import json
from copy import copy

from django.conf import settings
from django.contrib.gis.db import models


class BaseModel(models.Model):
    """Абстрактная модель со стандартными полями для других моделей
    """
    author_create = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=True, blank=True, on_delete=models.SET_NULL, related_name='%(app_label)s_%(class)s_author_create', verbose_name='Автор создания')
    author_update = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=True, blank=True, on_delete=models.SET_NULL, related_name='%(app_label)s_%(class)s_author_update', verbose_name='Автор обновления')
    dt_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    dt_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class HistoryManager(models.Manager):
    def __init__(self, model, instance=None):
        super(HistoryManager, self).__init__()
        self.model = model
        self.instance = instance

    def get_query_set(self):
        if self.instance is None:
            return super(HistoryManager, self).get_query_set()
        filter = {self.instance._meta.pk.name: self.instance.pk}
        return super(HistoryManager, self).get_query_set().filter(**filter)


class HistoryDescriptor(object):
    def __init__(self, model):
        self.model = model

    def __get__(self, instance, owner):
        if instance is None:
            return HistoryManager(self.model)
        return HistoryManager(self.model, instance)

class HistoryRecords(object):
    """Логирование любой модели
       в модель добавляем history = HistoryRecords()
       делаем manage.py makemigrations + manage.py migrate,
       чтобы создались модели для логирования
       Дальше просто пользуемся менеджером свойства,
       например, model.history.objects.all()
    """
    registry = {}
    
    def __init__(self, exclude = None, include = None):
        self.exclude = exclude
        self.include = include
    
    def contribute_to_class(self, cls, name):
        self.manager_name = name
        models.signals.class_prepared.connect(self.finalize, sender=cls)

    def finalize(self, sender, **kwargs):
        history_model = self.create_history_model(sender)

        models.signals.pre_save.connect(self.pre_save, sender=sender, weak=False)
        models.signals.post_delete.connect(self.post_delete, sender=sender, weak=False)
        models.signals.post_save.connect(self.post_save, sender=sender, weak=False)

        descriptor = HistoryDescriptor(history_model)
        setattr(sender, self.manager_name, descriptor)

    def create_history_model(self, model):
        attrs = self.get_history_model_fields(model)
        attrs.update(Meta=type('Meta', (), {
            'ordering': ('-history_date', ),
            'get_latest_by': 'history_date',
            'app_label': model._meta.app_label,
        }))
        name = 'History%s' % model._meta.object_name
        history_model =  type(name, (models.Model, ), attrs)
        self.__class__.registry[model._meta.object_name] = history_model
        return history_model
    
    def __contains__(self, object_name):
        return object_name in self.__class__.registry
    
    def get_history_model(self, object_name):
        return self.__class__.registry.get(object_name)

    def get_history_model_fields(self, model):
        fields =  {
            '__module__': model.__module__,
            'history_id': models.AutoField(primary_key=True),
            'history_date': models.DateTimeField(auto_now_add=True, null=True, blank=True),
            'history_data': models.TextField(),
            'history_all_data': models.TextField(blank = True, null = True),
            'history_type': models.CharField(max_length=1, choices=(
                ('+', 'Created'),
                ('~', 'Changed'),
                ('-', 'Deleted'),
            )),
            'get_data': lambda self: json.loads(self.history_data.encode('utf-8')),
            'get_all_data': lambda self: json.loads(self.history_all_data.encode('utf-8')),
            'set_data': lambda self, data: setattr(self, 'data', json.dumps(data)),
        }

        pk_field = copy(model._meta.get_field(model._meta.pk.name))
        pk_field.__class__ = models.IntegerField
        pk_field._unique = False
        pk_field.primary_key = False
        pk_field.db_index = True
        fields[model._meta.pk.name] = pk_field
        return fields

    def pre_save(self, instance, **kwargs):
        if instance.pk:
            self.create_history_record(instance, '~')
        
    def post_save(self, instance, created, **kwargs):
        if created:
            self.create_history_record(instance, '+')

    def post_delete(self, instance, **kwargs):
        self.create_history_record(instance, '-')

    def create_history_record(self, instance, history_type):
        manager = getattr(instance, self.manager_name)
        
        attrs = {}
        attrs[instance._meta.pk.name] = getattr(instance, instance._meta.pk.name)

        history_data = {}
        history_all_data = {}
        if instance.pk and history_type != '-':
            old = instance.__class__._default_manager.get(pk = instance.pk)
            for field in instance._meta.fields:
                if (self.exclude and field.name in self.exclude) or (self.include and field.name not in self.include):
                    continue

                if field.editable and type(field) not in (models.ManyToManyField, ):
                    new_value = getattr(instance, field.attname)
                    old_value = getattr(old, field.attname)
                    history_all_data[field.attname] = new_value
                    if new_value != old_value:
                        history_data[field.attname] = (old_value, new_value)
                        
        manager.create(history_type=history_type,
            history_data = json.dumps(history_data),
            history_all_data = json.dumps(history_all_data),
            **attrs)
