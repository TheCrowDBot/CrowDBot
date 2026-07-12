from crawio.parser import parse_er_diagram
from crawio.generator import (
    ERDiagramGenerator,
    Entity as DrawioEntity,
    Attribute as DrawioAttribute,
    Relationship as DrawioRelationship,
)
from crowdbot.services.path_utils import get_output_folder


class CrawIOPipeline:
    name = "crawio"

    def _save_result(
        self,
        generator: ERDiagramGenerator,
        image_path,
        output_dir,
    ):
        output_folder, image_name = get_output_folder(
            image_path,
            output_dir,
        )

        output_file = output_folder / f"{image_name}.drawio"

        generator.save_to_file(str(output_file))

        return output_file

    def run(
        self,
        matcher,
        image_path,
        output_dir="out",
        outputs=None,
        **kwargs,
    ):
        if matcher is None:
            raise ValueError("Missing matcher result")

        schema = parse_er_diagram(matcher, DEBUG=False)
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

        if output_dir and outputs and outputs.get("drawio", False):
            self._save_result(generator, image_path, output_dir)

        return generator
