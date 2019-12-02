from jinja2 import Environment, PackageLoader, select_autoescape

class HtmlBuilder():

    def __init__(self):
        self.Env = Environment(
            loader=PackageLoader('Modules','templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def BuildTemplate(self, template_name, template_data):
        template = self.Env.get_template(template_name)
        return template.render(data=template_data)