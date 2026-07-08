from crawio.parser import parse_er_diagram
from crawio.generator import (
    ERDiagramGenerator,
    Entity as DrawioEntity,
    Attribute as DrawioAttribute,
)


class CrawIOPipeline:
    def run(self, json):
        schema = parse_er_diagram(json)

        generator = ERDiagramGenerator()

        for entity in schema.entities:

            attributes = [
                DrawioAttribute(
                    name=attribute.name,
                    is_pk=attribute.is_pk,
                    is_fk=attribute.is_fk,
                )
                for attribute in entity.attributes
            ]

            drawio_entity = DrawioEntity(
                name=entity.name,
                attributes=attributes,
            )

            generator.add_entity(drawio_entity)

        for relationship in schema.relationships:
            generator.add_relationship(relationship)

        generator.save_to_file("diagram.drawio")

        return generator
