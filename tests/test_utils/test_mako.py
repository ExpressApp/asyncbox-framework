from asyncbox.utils.mako import TemplateFormatterLookup


def test_mako():
    template_lookup = TemplateFormatterLookup(
        directories=["tests/test_utils"], input_encoding="utf-8"
    )
    template = template_lookup.get_template

    text = template("template.mako").format(var1="var1", var2="var2")
    assert text == "var1\nvar2"
