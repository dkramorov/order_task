from django import forms


class OrderForm(forms.ModelForm):

    total_positions = forms.CharField(required=False, widget=forms.TextInput(attrs={'disabled': 'disabled', 'readonly': True}), label='Сумма позиций по всем наименованиям')
    positions_codes = forms.CharField(required=False, widget=forms.TextInput(attrs={'disabled': 'disabled', 'readonly': True, 'style': 'width:100%'}), label='Коды наименований')
    class Meta:
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            kwargs['initial'] = {'total_positions': instance.total_positions, 'positions_codes': instance.positions_codes}
        super().__init__(*args, **kwargs)



