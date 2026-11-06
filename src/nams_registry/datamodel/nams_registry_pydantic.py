from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "1.12.0"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )





class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'nams_registry',
     'default_range': 'string',
     'description': 'This is a repository of NAM and NAM-adjacent sources '
                    'collected in support of a NAMs landscape analysis.\n'
                    '\n'
                    'Sources are not limited to data repositories and knowledge '
                    'bases. They\n'
                    'also include reports, such as landscape analyses, reviews, '
                    'and OECD Test\n'
                    'Guidelines. Primary research papers are not included.',
     'id': 'https://w3id.org/monarch-initiative/nams-registry',
     'imports': ['linkml:types'],
     'license': 'MIT',
     'name': 'nams-registry',
     'prefixes': {'dcterms': {'prefix_prefix': 'dcterms',
                              'prefix_reference': 'http://purl.org/dc/terms/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'nams_registry': {'prefix_prefix': 'nams_registry',
                                    'prefix_reference': 'https://w3id.org/monarch-initiative/nams-registry/'},
                  'pav': {'prefix_prefix': 'pav',
                          'prefix_reference': 'http://purl.org/pav/'},
                  'schema': {'prefix_prefix': 'schema',
                             'prefix_reference': 'http://schema.org/'}},
     'see_also': ['https://monarch-initiative.github.io/nams-registry'],
     'source_file': 'src/nams_registry/schema/nams_registry.yaml',
     'title': 'nams-registry'} )

class ActivityStatusEnum(str, Enum):
    """
    The status of a resource. The same values as KG-Registry, which follow OBO Foundry.
    """
    active = "active"
    """
    The resource is active and available.
    """
    inactive = "inactive"
    """
    The resource is inactive. Its availability may vary.
    """
    orphaned = "orphaned"
    """
    The resource is not actively maintained. Its availability may vary.
    """
    unresponsive = "unresponsive"
    """
    The resource is no longer accessible. Only its metadata is available.
    """
    unknown = "unknown"
    """
    The status of the resource is unknown.
    """


class ResourceTypeEnum(str, Enum):
    """
    What form a resource takes. The KG-Registry Resource categories, plus Report.
    """
    DataSource = "DataSource"
    """
    A data source.
    """
    KnowledgeGraph = "KnowledgeGraph"
    """
    A heterogeneous collection of data represented as nodes (entities) and edges (relationships) between them.
    """
    Aggregator = "Aggregator"
    """
    An aggregator of data sources. It may be a data source itself, and its content may change in the process of aggregation.
    """
    Ontology = "Ontology"
    """
    A formal representation of the concepts in a domain and the relationships between them.
    """
    DataModel = "DataModel"
    """
    A formal representation of the concepts and relationships in a domain that defines how data is structured.
    """
    Report = "Report"
    """
    A report that surveys NAMs or sets out how a method is to be used, such as a landscape analysis, a review article, or an OECD Test Guideline. A primary research paper is not a report. Not one of the KG-Registry categories.
    """


class DomainAreaEnum(str, Enum):
    """
    Domains a resource covers. Taken from the KG-Registry domains used by its NAMs resources; add a value here when a new resource needs one.
    """
    adverse_outcome_pathways = "adverse outcome pathways"
    """
    Adverse outcome pathways linking molecular initiating events to adverse outcomes.
    """
    anatomy_and_development = "anatomy and development"
    """
    The anatomy and development of organisms, including their structure, morphology, and developmental biology.
    """
    biological_systems = "biological systems"
    """
    The biological sciences broadly, including cellular and molecular biology and other biological disciplines not better described by a more specific domain.
    """
    biomedical = "biomedical"
    """
    The biomedical sciences broadly, spanning the study of biological systems in the context of health and disease. Use a more specific domain (e.g., clinical) where one applies.
    """
    cell_biology = "cell biology"
    """
    Cells and cell types, including cell lines, cell markers, and subcellular structures.
    """
    cheminformatics = "cheminformatics"
    """
    Computational representation, identification, and classification of chemical structures.
    """
    chemistry_and_biochemistry = "chemistry and biochemistry"
    """
    The chemical and biochemical sciences, including the structure, properties, and reactions of chemical compounds.
    """
    clinical = "clinical"
    """
    The clinical sciences concerned with the care of patients, including clinical trials, patient data, and diagnosis and treatment of disease.
    """
    clinical_trials = "clinical trials"
    """
    Clinical trials, including trial registries and the data standards used to report them.
    """
    drug_discovery = "drug discovery"
    """
    The process of identifying and developing new candidate medications, including target identification, validation, and compound screening.
    """
    drug_interactions = "drug interactions"
    """
    Interactions between drugs and between drugs and foods or natural products.
    """
    ecology = "ecology"
    """
    The interactions of organisms with each other and their environment, including ecological networks.
    """
    environment = "environment"
    """
    The environment and ecosystems, including ecology and environmental health.
    """
    environmental_exposure = "environmental exposure"
    """
    Exposure of people and organisms to environmental agents and the health effects of those exposures.
    """
    epigenomics = "epigenomics"
    """
    Genome-wide chromatin state and organization, including chromatin conformation and regulatory element annotation.
    """
    gene_expression_profiling = "gene expression profiling"
    """
    Measurement of gene expression across tissues, cells, and conditions, including transcriptomic signatures.
    """
    genetic_variation = "genetic variation"
    """
    Germline and somatic genetic variants, including their frequencies, effects, and clinical interpretation.
    """
    genomics = "genomics"
    """
    The study of genomes, including genome structure, evolution, function, mapping, and editing.
    """
    high_throughput_screening = "high-throughput screening"
    """
    Large-scale screening of chemical or genetic perturbations, including cell line sensitivity and perturbation profiling.
    """
    information_technology = "information technology"
    """
    The information technology and informatics sciences, including software, computational methods, simulation and modeling, and digital health technologies.
    """
    machine_learning = "machine learning"
    """
    Machine learning and artificial intelligence, including AI-ready data and models.
    """
    molecular_evolution = "molecular evolution"
    """
    The evolution of genes and proteins, including orthology, gene families, and comparative analysis.
    """
    pathways = "pathways"
    """
    Biological pathways, including metabolic, signaling, and regulatory networks that control cellular processes.
    """
    pharmacology = "pharmacology"
    """
    The study of how drugs interact with biological systems, including drug discovery, development, and therapeutic uses.
    """
    protein_structure = "protein structure"
    """
    The three-dimensional structure of proteins, whether determined experimentally or predicted.
    """
    proteomics = "proteomics"
    """
    The large-scale study of proteins, their structures, functions, and interactions.
    """
    public_health = "public health"
    """
    The science of protecting and improving the health of people and their communities, including epidemiology, population health, and the social determinants of health.
    """
    rare_disease = "rare disease"
    """
    Rare diseases, including rare Mendelian and other genetic disorders, their phenotypes, genes, and treatments.
    """
    single_cell_analysis = "single-cell analysis"
    """
    Data and methods that measure molecules in individual cells, including single-cell and spatial atlases.
    """
    software = "software"
    """
    Software, including package registries, software supply chains, and vulnerabilities.
    """
    systems_biology = "systems biology"
    """
    The computational and mathematical analysis of complex biological systems and their interactions.
    """
    toxicology = "toxicology"
    """
    The study of the adverse effects of chemicals on living organisms.
    """


class HoldsNAMsEnum(str, Enum):
    """
    Whether a resource holds NAMs, and whether they are its primary content.
    """
    primary = "primary"
    """
    NAMs, or records produced with them such as methods, models, cell lines, or assay data, are the resource's primary content.
    """
    secondary = "secondary"
    """
    The resource holds NAMs, but they are not its primary content.
    """
    none = "none"
    """
    The resource holds no NAMs.
    """
    unclear = "unclear"
    """
    The resource was evaluated, but whether it holds NAMs could not be decided. Explain why in relevance_note.
    """


class CurationModelEnum(str, Enum):
    """
    Who creates a resource's content.
    """
    maintainers = "maintainers"
    """
    The resource's own team creates or curates the content, e.g. the ToxCast assay annotations curated by EPA.
    """
    community = "community"
    """
    Open contributors create the content, wiki-style, e.g. AOP-Wiki.
    """
    depositors = "depositors"
    """
    Authors or labs submit records about their own work, e.g. model submissions to BioModels.
    """
    automated = "automated"
    """
    A pipeline generates or transforms the content, e.g. BioBricks repackaging another resource.
    """
    aggregated = "aggregated"
    """
    The content is copied from other resources.
    """


class PriorityEnum(str, Enum):
    """
    Extraction priority: how much a resource adds, and so how soon it is worth extracting content from.
    """
    high = "high"
    medium = "medium"
    low = "low"


class SourceRegistryEnum(str, Enum):
    """
    Registries that content can be imported from.
    """
    kg_registry = "kg_registry"
    """
    KG-Registry, the Knowledge Graph Hub registry.
    """



class NamedThing(ConfiguredBaseModel):
    """
    A generic grouping for any identifiable entity
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'schema:Thing',
         'from_schema': 'https://w3id.org/monarch-initiative/nams-registry'})

    id: str = Field(default=..., description="""The identifier of an entity within the registry. Use the KG-Registry id where the resource has one, e.g. toxcast. For an OECD Test Guideline, use oecd-tg- followed by the guideline number in lower case, e.g. oecd-tg-442d.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing', 'LicenseInfo', 'Publication'],
         'slot_uri': 'schema:identifier'} })
    name: str = Field(default=..., description="""The human-readable name of the resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing'], 'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""A description of the resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing'], 'slot_uri': 'schema:description'} })


class Resource(NamedThing):
    """
    A source of NAMs or NAMs-adjacent information. This includes data resources, such as databases, repositories, catalogs, and portals, and reports, such as landscape analyses, reviews, and OECD Test Guidelines.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/monarch-initiative/nams-registry'})

    synonyms: Optional[list[str]] = Field(default=None, description="""Acronyms, abbreviations, and other alternate names for the resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Resource']} })
    homepage_url: Optional[str] = Field(default=None, description="""The primary URL of the resource, preferably the main page documenting it.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Resource'], 'slot_uri': 'schema:url'} })
    repository: Optional[str] = Field(default=None, description="""The main version control repository for the resource, if it has one.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Resource']} })
    resource_type: Optional[ResourceTypeEnum] = Field(default=None, description="""What form the resource takes, such as a data source or a knowledge graph. Imported from the KG-Registry category.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Resource']} })
    domain_areas: Optional[list[DomainAreaEnum]] = Field(default=None, description="""The domains the resource covers, such as toxicology. Imported from the KG-Registry domains.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Resource']} })
    holds_nams: Optional[HoldsNAMsEnum] = Field(default=None, description="""Whether the resource holds NAMs, and whether they are its primary content. Leave it out until the resource has been evaluated.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Resource']} })
    relevance_note: Optional[str] = Field(default=None, description="""Why the resource was given its holds_nams value, e.g. \"Holds the measurement methods for key events, but its primary content is adverse outcome pathways.\"""", json_schema_extra = { "linkml_meta": {'domain_of': ['Resource']} })
    curation_model: Optional[list[CurationModelEnum]] = Field(default=None, description="""Who creates the resource's content, as the resource works today. Use more than one value when the resource mixes them.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Resource']} })
    dismech_integration: Optional[str] = Field(default=None, description="""The resource's current state in DisMech: whether any of its content has been incorporated into DisMech, and whether DisMech has tooling for it, such as a script or skill. Records what exists, not what the resource could offer. Free text for now.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Resource']} })
    priority: Optional[PriorityEnum] = Field(default=None, description="""Extraction priority: how much the resource adds, and so how soon it is worth extracting content from. Set it once that has been investigated. A resource that repackages another one can still add value, for example through a new format, integration with other data, or easier access, so repackaging alone does not make a resource low priority.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Resource']} })
    priority_rationale: Optional[str] = Field(default=None, description="""Why the resource was given its priority, based on what was found about what it adds. For a resource that repackages another, say what it adds beyond the original, or that nothing was found.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Resource']} })
    discussion_issue: Optional[str] = Field(default=None, description="""The GitHub issue where the resource is discussed, e.g. https://github.com/monarch-initiative/nams-registry/issues/2. Set by `just create-review-issues`.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Resource']} })
    activity_status: Optional[ActivityStatusEnum] = Field(default=None, description="""The status of the resource itself.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Resource']} })
    use_instead: Optional[list[str]] = Field(default=None, description="""The ids of other registry resources to use in place of this one, for a resource that is no longer active and has a clear replacement.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Resource']} })
    license: Optional[LicenseInfo] = Field(default=None, description="""The license of the resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Resource'], 'slot_uri': 'dcterms:license'} })
    publications: Optional[list[Publication]] = Field(default=None, description="""For a Report, the publications the report consists of. For any other resource, publications that describe the resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Resource']} })
    creation_date: Optional[date] = Field(default=None, description="""The date this registry entry was created, not the date the resource was created. For an entry imported from another registry, the date of the import.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Resource'], 'slot_uri': 'dcterms:created'} })
    last_modified_date: Optional[date] = Field(default=None, description="""The date this registry entry was last changed, not the date the resource was last updated.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Resource'], 'slot_uri': 'dcterms:modified'} })
    imported_from: Optional[list[ImportRecord]] = Field(default=None, description="""The registries this entry's content was imported from. Leave empty for an entry curated directly in this registry.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Resource'], 'slot_uri': 'pav:importedFrom'} })
    id: str = Field(default=..., description="""The identifier of an entity within the registry. Use the KG-Registry id where the resource has one, e.g. toxcast. For an OECD Test Guideline, use oecd-tg- followed by the guideline number in lower case, e.g. oecd-tg-442d.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing', 'LicenseInfo', 'Publication'],
         'slot_uri': 'schema:identifier'} })
    name: str = Field(default=..., description="""The human-readable name of the resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing'], 'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""A description of the resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing'], 'slot_uri': 'schema:description'} })

    @field_validator('discussion_issue')
    def pattern_discussion_issue(cls, v):
        pattern=re.compile(r"^https://github\.com/monarch-initiative/nams-registry/issues/\d+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid discussion_issue format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid discussion_issue format: {v}"
            raise ValueError(err_msg)
        return v


class LicenseInfo(ConfiguredBaseModel):
    """
    A license for a resource.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/monarch-initiative/nams-registry'})

    id: Optional[str] = Field(default=None, description="""A URL to the license text, e.g. https://creativecommons.org/licenses/by/4.0/. Leave it out when there is none, as for a US government work.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing', 'LicenseInfo', 'Publication']} })
    label: str = Field(default=..., description="""The name of the license.""", json_schema_extra = { "linkml_meta": {'domain_of': ['LicenseInfo']} })


class Publication(ConfiguredBaseModel):
    """
    A publication. The same structure as a KG-Registry Publication.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/monarch-initiative/nams-registry'})

    id: str = Field(default=..., description="""A CURIE for the publication, such as a DOI with its prefix (doi:10.1038/s41597-021-00962-3) or a PMID.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing', 'LicenseInfo', 'Publication']} })
    title: Optional[str] = Field(default=None, description="""The title of the publication.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Publication']} })
    authors: Optional[list[str]] = Field(default=None, description="""The authors, e.g. Mortensen HM.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Publication']} })
    journal: Optional[str] = Field(default=None, description="""The journal the publication appeared in.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Publication']} })
    year: Optional[str] = Field(default=None, description="""The year of publication, e.g. '2021'.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Publication']} })
    doi: Optional[str] = Field(default=None, description="""The DOI, without a prefix.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Publication']} })
    preferred: Optional[bool] = Field(default=None, description="""Whether this is the publication to cite for the resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Publication']} })

    @field_validator('year')
    def pattern_year(cls, v):
        pattern=re.compile(r"^\d{4}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid year format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid year format: {v}"
            raise ValueError(err_msg)
        return v


class ImportRecord(ConfiguredBaseModel):
    """
    A record of content imported into this registry entry from another registry.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/monarch-initiative/nams-registry'})

    source: SourceRegistryEnum = Field(default=..., description="""The registry the content was imported from.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ImportRecord']} })
    source_id: str = Field(default=..., description="""The resource's identifier in the source registry, e.g. toxcast.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ImportRecord']} })
    source_url: Optional[str] = Field(default=None, description="""The URL of the resource's page in the source registry.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ImportRecord'], 'slot_uri': 'pav:sourceAccessedAt'} })
    source_version: Optional[str] = Field(default=None, description="""The version of the source registry the content was copied from. For a registry kept in git, such as KG-Registry, the commit hash.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ImportRecord']} })
    imported_on: date = Field(default=..., description="""The date the content was imported.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ImportRecord'], 'slot_uri': 'pav:importedOn'} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
NamedThing.model_rebuild()
Resource.model_rebuild()
LicenseInfo.model_rebuild()
Publication.model_rebuild()
ImportRecord.model_rebuild()
