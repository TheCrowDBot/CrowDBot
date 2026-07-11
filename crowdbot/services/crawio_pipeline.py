from crawio.parser import parse_er_diagram
from crawio.generator import (
    ERDiagramGenerator,
    Entity as DrawioEntity,
    Attribute as DrawioAttribute,
    Relationship as DrawioRelationship,
)


class CrawIOPipeline:

    def run(self, json):
        schema = parse_er_diagram(json, DEBUG=True)
        for e in schema.entities:
            print("ENTITY:", e.name, "| ATTRS:", [a.name for a in e.attributes])
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
                id=entity.id,
                name=entity.name,
                attributes=attributes,
                x=entity.x,
                y=entity.y,
                # width=entity.width,
                # height=entity.height,
            )

            generator.add_entity(drawio_entity)

        for relationship in schema.relationships:
            drawio_relationship = DrawioRelationship(
                source=relationship.source,
                target=relationship.target,
                source_cardinality=relationship.source_cardinality,
                target_cardinality=relationship.target_cardinality,
                from_attribute=relationship.source_attribute,
                to_attribute=relationship.target_attribute,
            )

            generator.add_relationship(drawio_relationship)

        generator.save_to_file("diagram.drawio")

        return generator
