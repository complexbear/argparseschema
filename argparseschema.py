""" 
Module to convert argparse parsers into marshmallow  
schemas for use in web services.

Making it easy to convert cmd line scripts into services.
"""
import argparse
import marshmallow as ma


def type_to_field(t):
    """ Returns a marshmallow Field instance
        of the correct type.
    """
    type_map = dict(
        int=ma.fields.Int,
        str=ma.fields.Str,
        bool=ma.fields.Bool,
    )
    return ma.fields.Str if t is None else type_map[t.__name__]


def parser_to_schema(parser, name):
    """
    :param parser: An argparse parser to convert to a schema
    :return: A marshmallow schema class representing the fields of the parser
    """
    attrs = {}
    for arg in parser._actions:
        if isinstance(arg, (
                argparse._StoreAction, 
                argparse._StoreTrueAction,
                argparse._StoreFalseAction
            )
        ):
            field_args = dict(
                required=arg.required,
                default=arg.default,
                missing=arg.default,
                description=arg.help,
                validator=lambda val: type(val) == arg.type
            )
            attrs[arg.dest] = type_to_field(arg.type)(**field_args)

    schema = type(name, (ma.Schema,), attrs)
    return schema


