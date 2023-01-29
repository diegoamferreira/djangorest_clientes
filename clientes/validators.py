import re

from validate_docbr import CPF


def cpf_valido(cpf):
    cpf_validator = CPF()

    # Validar CPF
    return cpf_validator.validate(cpf)  # True


def nome_valido(nome):
    return nome.isalpha()


def rg_valido(rg):
    return len(rg) == 9


def celular_valido(celular):
    """Check cell number using regex"""
    modelo = r'[0-9]{2} [0-9]{5}-[0-9]{4}'
    pattern = re.compile(modelo)
    return bool(pattern.match(celular))
