from ._templates import (
    _DATA
    )

from bs4 import BeautifulSoup



def _process_template_params(params):
    new_params = {}

    for _key, _value in params.items():
        _value = str(_value)

        
        #Tirar espaços desnecessarios.
        _value = _value.strip().replace('\n\n\n', '\n\n')

        if not 'allow_html' in _key:
            #Remover tags html do valor do parametro;   
            _value = BeautifulSoup(_value, "lxml").text

        """
        Remove custom parameters from _key;
        """
        _key = (
            _key.replace('allow_html', ''
                ).replace('?', '').replace('&', '')
            )

        """
        Atualizar valor do parametro no {}
        """
        new_params[_key] = _value

    return new_params


def get_template(
    template,
    params={}
    ):
    template = _DATA.get(template)

    if not template:
        raise ValueError('Template not found')

    if params:
        params = _process_template_params(params)

    template_formated = template.format(**params)
    return template_formated