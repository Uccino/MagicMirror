from jinja2 import Environment, PackageLoader, select_autoescape

class HtmlBuilder():

    def __init__(self):
        """Provides functions to build HTML markup with jinja2
        """        
        self.Env = Environment(
            loader=PackageLoader('Modules','templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def BuildTemplate(self, template_name, template_data):
        """Builds a template with the given data
        
        Arguments:
            template_name {[string]} -- [Name of the template to be rendered]

            template_data {[dict]} -- [Data to be rendered in the template]
        
        Returns:
            [type] -- [description]
        """        
        template = self.Env.get_template(template_name)
        return template.render(data=template_data)