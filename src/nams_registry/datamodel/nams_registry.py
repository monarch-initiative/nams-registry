# Auto generated from nams_registry.yaml by pythongen.py version: 0.0.1
# Schema: nams-registry
#
# id: https://w3id.org/monarch-initiative/nams-registry
# description: This is a repository of NAM and NAM-adjacent sources collected in support of a NAMs landscape analysis.
#
#   Sources are not limited to data repositories and knowledge bases. They
#   also include reports, such as landscape analyses, reviews, and OECD Test
#   Guidelines. Primary research papers are not included.
# license: MIT

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, Date, String, Uri, Uriorcurie
from linkml_runtime.utils.metamodelcore import Bool, URI, URIorCURIE, XSDDate

metamodel_version = "1.12.0"
version = None

# Namespaces
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
NAMS_REGISTRY = CurieNamespace('nams_registry', 'https://w3id.org/monarch-initiative/nams-registry/')
PAV = CurieNamespace('pav', 'http://purl.org/pav/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
DEFAULT_ = NAMS_REGISTRY


# Types

# Class references
class NamedThingId(extended_str):
    pass


class ResourceId(NamedThingId):
    pass


class PublicationId(URIorCURIE):
    pass


@dataclass(repr=False)
class NamedThing(YAMLRoot):
    """
    A generic grouping for any identifiable entity
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["Thing"]
    class_class_curie: ClassVar[str] = "schema:Thing"
    class_name: ClassVar[str] = "NamedThing"
    class_model_uri: ClassVar[URIRef] = NAMS_REGISTRY.NamedThing

    id: Union[str, NamedThingId] = None
    name: str = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NamedThingId):
            self.id = NamedThingId(self.id)

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Resource(NamedThing):
    """
    A source of NAMs or NAMs-adjacent information. This includes data resources, such as databases, repositories,
    catalogs, and portals, and reports, such as landscape analyses, reviews, and OECD Test Guidelines.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NAMS_REGISTRY["Resource"]
    class_class_curie: ClassVar[str] = "nams_registry:Resource"
    class_name: ClassVar[str] = "Resource"
    class_model_uri: ClassVar[URIRef] = NAMS_REGISTRY.Resource

    id: Union[str, ResourceId] = None
    name: str = None
    nams_relevance: Union[str, "NAMsRelevanceEnum"] = None
    synonyms: Optional[Union[str, list[str]]] = empty_list()
    homepage_url: Optional[Union[str, URI]] = None
    repository: Optional[Union[str, URI]] = None
    resource_type: Optional[Union[str, "ResourceTypeEnum"]] = None
    domain_areas: Optional[Union[Union[str, "DomainAreaEnum"], list[Union[str, "DomainAreaEnum"]]]] = empty_list()
    relevance_note: Optional[str] = None
    curation_model: Optional[Union[Union[str, "CurationModelEnum"], list[Union[str, "CurationModelEnum"]]]] = empty_list()
    dismech_integration: Optional[str] = None
    priority: Optional[Union[str, "PriorityEnum"]] = None
    priority_rationale: Optional[str] = None
    discussion_issue: Optional[Union[str, URI]] = None
    activity_status: Optional[Union[str, "ActivityStatusEnum"]] = None
    use_instead: Optional[Union[Union[str, ResourceId], list[Union[str, ResourceId]]]] = empty_list()
    license: Optional[Union[dict, "LicenseInfo"]] = None
    publications: Optional[Union[dict[Union[str, PublicationId], Union[dict, "Publication"]], list[Union[dict, "Publication"]]]] = empty_dict()
    creation_date: Optional[Union[str, XSDDate]] = None
    last_modified_date: Optional[Union[str, XSDDate]] = None
    imported_from: Optional[Union[Union[dict, "ImportRecord"], list[Union[dict, "ImportRecord"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ResourceId):
            self.id = ResourceId(self.id)

        if self._is_empty(self.nams_relevance):
            self.MissingRequiredField("nams_relevance")
        if not isinstance(self.nams_relevance, NAMsRelevanceEnum):
            self.nams_relevance = NAMsRelevanceEnum(self.nams_relevance)

        if not isinstance(self.synonyms, list):
            self.synonyms = [self.synonyms] if self.synonyms is not None else []
        self.synonyms = [v if isinstance(v, str) else str(v) for v in self.synonyms]

        if self.homepage_url is not None and not isinstance(self.homepage_url, URI):
            self.homepage_url = URI(self.homepage_url)

        if self.repository is not None and not isinstance(self.repository, URI):
            self.repository = URI(self.repository)

        if self.resource_type is not None and not isinstance(self.resource_type, ResourceTypeEnum):
            self.resource_type = ResourceTypeEnum(self.resource_type)

        if not isinstance(self.domain_areas, list):
            self.domain_areas = [self.domain_areas] if self.domain_areas is not None else []
        self.domain_areas = [v if isinstance(v, DomainAreaEnum) else DomainAreaEnum(v) for v in self.domain_areas]

        if self.relevance_note is not None and not isinstance(self.relevance_note, str):
            self.relevance_note = str(self.relevance_note)

        if not isinstance(self.curation_model, list):
            self.curation_model = [self.curation_model] if self.curation_model is not None else []
        self.curation_model = [v if isinstance(v, CurationModelEnum) else CurationModelEnum(v) for v in self.curation_model]

        if self.dismech_integration is not None and not isinstance(self.dismech_integration, str):
            self.dismech_integration = str(self.dismech_integration)

        if self.priority is not None and not isinstance(self.priority, PriorityEnum):
            self.priority = PriorityEnum(self.priority)

        if self.priority_rationale is not None and not isinstance(self.priority_rationale, str):
            self.priority_rationale = str(self.priority_rationale)

        if self.discussion_issue is not None and not isinstance(self.discussion_issue, URI):
            self.discussion_issue = URI(self.discussion_issue)

        if self.activity_status is not None and not isinstance(self.activity_status, ActivityStatusEnum):
            self.activity_status = ActivityStatusEnum(self.activity_status)

        if not isinstance(self.use_instead, list):
            self.use_instead = [self.use_instead] if self.use_instead is not None else []
        self.use_instead = [v if isinstance(v, ResourceId) else ResourceId(v) for v in self.use_instead]

        if self.license is not None and not isinstance(self.license, LicenseInfo):
            self.license = LicenseInfo(**as_dict(self.license))

        self._normalize_inlined_as_list(slot_name="publications", slot_type=Publication, key_name="id", keyed=True)

        if self.creation_date is not None and not isinstance(self.creation_date, XSDDate):
            self.creation_date = XSDDate(self.creation_date)

        if self.last_modified_date is not None and not isinstance(self.last_modified_date, XSDDate):
            self.last_modified_date = XSDDate(self.last_modified_date)

        self._normalize_inlined_as_list(slot_name="imported_from", slot_type=ImportRecord, key_name="source", keyed=False)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class LicenseInfo(YAMLRoot):
    """
    A license for a resource.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NAMS_REGISTRY["LicenseInfo"]
    class_class_curie: ClassVar[str] = "nams_registry:LicenseInfo"
    class_name: ClassVar[str] = "LicenseInfo"
    class_model_uri: ClassVar[URIRef] = NAMS_REGISTRY.LicenseInfo

    label: str = None
    id: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.label):
            self.MissingRequiredField("label")
        if not isinstance(self.label, str):
            self.label = str(self.label)

        if self.id is not None and not isinstance(self.id, URI):
            self.id = URI(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Publication(YAMLRoot):
    """
    A publication. The same structure as a KG-Registry Publication.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NAMS_REGISTRY["Publication"]
    class_class_curie: ClassVar[str] = "nams_registry:Publication"
    class_name: ClassVar[str] = "Publication"
    class_model_uri: ClassVar[URIRef] = NAMS_REGISTRY.Publication

    id: Union[str, PublicationId] = None
    title: Optional[str] = None
    authors: Optional[Union[str, list[str]]] = empty_list()
    journal: Optional[str] = None
    year: Optional[str] = None
    doi: Optional[str] = None
    preferred: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PublicationId):
            self.id = PublicationId(self.id)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if not isinstance(self.authors, list):
            self.authors = [self.authors] if self.authors is not None else []
        self.authors = [v if isinstance(v, str) else str(v) for v in self.authors]

        if self.journal is not None and not isinstance(self.journal, str):
            self.journal = str(self.journal)

        if self.year is not None and not isinstance(self.year, str):
            self.year = str(self.year)

        if self.doi is not None and not isinstance(self.doi, str):
            self.doi = str(self.doi)

        if self.preferred is not None and not isinstance(self.preferred, Bool):
            self.preferred = Bool(self.preferred)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ImportRecord(YAMLRoot):
    """
    A record of content imported into this registry entry from another registry.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NAMS_REGISTRY["ImportRecord"]
    class_class_curie: ClassVar[str] = "nams_registry:ImportRecord"
    class_name: ClassVar[str] = "ImportRecord"
    class_model_uri: ClassVar[URIRef] = NAMS_REGISTRY.ImportRecord

    source: Union[str, "SourceRegistryEnum"] = None
    source_id: str = None
    imported_on: Union[str, XSDDate] = None
    source_url: Optional[Union[str, URI]] = None
    source_version: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.source):
            self.MissingRequiredField("source")
        if not isinstance(self.source, SourceRegistryEnum):
            self.source = SourceRegistryEnum(self.source)

        if self._is_empty(self.source_id):
            self.MissingRequiredField("source_id")
        if not isinstance(self.source_id, str):
            self.source_id = str(self.source_id)

        if self._is_empty(self.imported_on):
            self.MissingRequiredField("imported_on")
        if not isinstance(self.imported_on, XSDDate):
            self.imported_on = XSDDate(self.imported_on)

        if self.source_url is not None and not isinstance(self.source_url, URI):
            self.source_url = URI(self.source_url)

        if self.source_version is not None and not isinstance(self.source_version, str):
            self.source_version = str(self.source_version)

        super().__post_init__(**kwargs)


# Enumerations
class ActivityStatusEnum(EnumDefinitionImpl):
    """
    The status of a resource. The same values as KG-Registry, which follow OBO Foundry.
    """
    active = PermissibleValue(
        text="active",
        description="The resource is active and available.")
    inactive = PermissibleValue(
        text="inactive",
        description="The resource is inactive. Its availability may vary.")
    orphaned = PermissibleValue(
        text="orphaned",
        description="The resource is not actively maintained. Its availability may vary.")
    unresponsive = PermissibleValue(
        text="unresponsive",
        description="The resource is no longer accessible. Only its metadata is available.")
    unknown = PermissibleValue(
        text="unknown",
        description="The status of the resource is unknown.")

    _defn = EnumDefinition(
        name="ActivityStatusEnum",
        description="The status of a resource. The same values as KG-Registry, which follow OBO Foundry.",
    )

class ResourceTypeEnum(EnumDefinitionImpl):
    """
    What form a resource takes. The KG-Registry Resource categories, plus Report.
    """
    DataSource = PermissibleValue(
        text="DataSource",
        description="A data source.")
    KnowledgeGraph = PermissibleValue(
        text="KnowledgeGraph",
        description="""A heterogeneous collection of data represented as nodes (entities) and edges (relationships) between them.""")
    Aggregator = PermissibleValue(
        text="Aggregator",
        description="""An aggregator of data sources. It may be a data source itself, and its content may change in the process of aggregation.""")
    Ontology = PermissibleValue(
        text="Ontology",
        description="A formal representation of the concepts in a domain and the relationships between them.")
    DataModel = PermissibleValue(
        text="DataModel",
        description="""A formal representation of the concepts and relationships in a domain that defines how data is structured.""")
    Report = PermissibleValue(
        text="Report",
        description="""A report that surveys NAMs or sets out how a method is to be used, such as a landscape analysis, a review article, or an OECD Test Guideline. A primary research paper is not a report. Not one of the KG-Registry categories.""")

    _defn = EnumDefinition(
        name="ResourceTypeEnum",
        description="What form a resource takes. The KG-Registry Resource categories, plus Report.",
    )

class DomainAreaEnum(EnumDefinitionImpl):
    """
    Domains a resource covers. Taken from the KG-Registry domains used by its NAMs resources; add a value here when a
    new resource needs one.
    """
    biomedical = PermissibleValue(
        text="biomedical",
        description="""The biomedical sciences broadly, spanning the study of biological systems in the context of health and disease. Use a more specific domain (e.g., clinical) where one applies.""")
    cheminformatics = PermissibleValue(
        text="cheminformatics",
        description="Computational representation, identification, and classification of chemical structures.")
    clinical = PermissibleValue(
        text="clinical",
        description="""The clinical sciences concerned with the care of patients, including clinical trials, patient data, and diagnosis and treatment of disease.""")
    ecology = PermissibleValue(
        text="ecology",
        description="""The interactions of organisms with each other and their environment, including ecological networks.""")
    environment = PermissibleValue(
        text="environment",
        description="The environment and ecosystems, including ecology and environmental health.")
    epigenomics = PermissibleValue(
        text="epigenomics",
        description="""Genome-wide chromatin state and organization, including chromatin conformation and regulatory element annotation.""")
    genomics = PermissibleValue(
        text="genomics",
        description="The study of genomes, including genome structure, evolution, function, mapping, and editing.")
    pathways = PermissibleValue(
        text="pathways",
        description="""Biological pathways, including metabolic, signaling, and regulatory networks that control cellular processes.""")
    pharmacology = PermissibleValue(
        text="pharmacology",
        description="""The study of how drugs interact with biological systems, including drug discovery, development, and therapeutic uses.""")
    proteomics = PermissibleValue(
        text="proteomics",
        description="The large-scale study of proteins, their structures, functions, and interactions.")
    software = PermissibleValue(
        text="software",
        description="Software, including package registries, software supply chains, and vulnerabilities.")
    toxicology = PermissibleValue(
        text="toxicology",
        description="The study of the adverse effects of chemicals on living organisms.")

    _defn = EnumDefinition(
        name="DomainAreaEnum",
        description="""Domains a resource covers. Taken from the KG-Registry domains used by its NAMs resources; add a value here when a new resource needs one.""",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "adverse outcome pathways",
            PermissibleValue(
                text="adverse outcome pathways",
                description="Adverse outcome pathways linking molecular initiating events to adverse outcomes."))
        setattr(cls, "anatomy and development",
            PermissibleValue(
                text="anatomy and development",
                description="""The anatomy and development of organisms, including their structure, morphology, and developmental biology."""))
        setattr(cls, "biological systems",
            PermissibleValue(
                text="biological systems",
                description="""The biological sciences broadly, including cellular and molecular biology and other biological disciplines not better described by a more specific domain."""))
        setattr(cls, "cell biology",
            PermissibleValue(
                text="cell biology",
                description="Cells and cell types, including cell lines, cell markers, and subcellular structures."))
        setattr(cls, "chemistry and biochemistry",
            PermissibleValue(
                text="chemistry and biochemistry",
                description="""The chemical and biochemical sciences, including the structure, properties, and reactions of chemical compounds."""))
        setattr(cls, "clinical trials",
            PermissibleValue(
                text="clinical trials",
                description="""Clinical trials, including trial registries and the data standards used to report them."""))
        setattr(cls, "drug discovery",
            PermissibleValue(
                text="drug discovery",
                description="""The process of identifying and developing new candidate medications, including target identification, validation, and compound screening."""))
        setattr(cls, "drug interactions",
            PermissibleValue(
                text="drug interactions",
                description="Interactions between drugs and between drugs and foods or natural products."))
        setattr(cls, "environmental exposure",
            PermissibleValue(
                text="environmental exposure",
                description="""Exposure of people and organisms to environmental agents and the health effects of those exposures."""))
        setattr(cls, "gene expression profiling",
            PermissibleValue(
                text="gene expression profiling",
                description="""Measurement of gene expression across tissues, cells, and conditions, including transcriptomic signatures."""))
        setattr(cls, "genetic variation",
            PermissibleValue(
                text="genetic variation",
                description="""Germline and somatic genetic variants, including their frequencies, effects, and clinical interpretation."""))
        setattr(cls, "high-throughput screening",
            PermissibleValue(
                text="high-throughput screening",
                description="""Large-scale screening of chemical or genetic perturbations, including cell line sensitivity and perturbation profiling."""))
        setattr(cls, "information technology",
            PermissibleValue(
                text="information technology",
                description="""The information technology and informatics sciences, including software, computational methods, simulation and modeling, and digital health technologies."""))
        setattr(cls, "machine learning",
            PermissibleValue(
                text="machine learning",
                description="Machine learning and artificial intelligence, including AI-ready data and models."))
        setattr(cls, "molecular evolution",
            PermissibleValue(
                text="molecular evolution",
                description="""The evolution of genes and proteins, including orthology, gene families, and comparative analysis."""))
        setattr(cls, "protein structure",
            PermissibleValue(
                text="protein structure",
                description="""The three-dimensional structure of proteins, whether determined experimentally or predicted."""))
        setattr(cls, "public health",
            PermissibleValue(
                text="public health",
                description="""The science of protecting and improving the health of people and their communities, including epidemiology, population health, and the social determinants of health."""))
        setattr(cls, "rare disease",
            PermissibleValue(
                text="rare disease",
                description="""Rare diseases, including rare Mendelian and other genetic disorders, their phenotypes, genes, and treatments."""))
        setattr(cls, "single-cell analysis",
            PermissibleValue(
                text="single-cell analysis",
                description="""Data and methods that measure molecules in individual cells, including single-cell and spatial atlases."""))
        setattr(cls, "systems biology",
            PermissibleValue(
                text="systems biology",
                description="""The computational and mathematical analysis of complex biological systems and their interactions."""))

class NAMsRelevanceEnum(EnumDefinitionImpl):
    """
    How a resource relates to NAMs.
    """
    holds_nams = PermissibleValue(
        text="holds_nams",
        description="""The resource holds NAMs or records produced with them: methods, models, cell lines, or assay data.""")
    points_to_nams = PermissibleValue(
        text="points_to_nams",
        description="""The resource holds no NAMs itself but helps find them, by listing, surveying, or citing NAMs held elsewhere, such as a landscape analysis or a catalog.""")
    nams_adjacent = PermissibleValue(
        text="nams_adjacent",
        description="""The resource supports work with NAMs but neither holds nor points to them, such as reference in vivo data used to benchmark NAMs or chemical identity data.""")
    undecided = PermissibleValue(
        text="undecided",
        description="The resource has not yet been reviewed.")

    _defn = EnumDefinition(
        name="NAMsRelevanceEnum",
        description="How a resource relates to NAMs.",
    )

class CurationModelEnum(EnumDefinitionImpl):
    """
    Who creates a resource's content.
    """
    maintainers = PermissibleValue(
        text="maintainers",
        description="""The resource's own team creates or curates the content, e.g. the ToxCast assay annotations curated by EPA.""")
    community = PermissibleValue(
        text="community",
        description="Open contributors create the content, wiki-style, e.g. AOP-Wiki.")
    depositors = PermissibleValue(
        text="depositors",
        description="Authors or labs submit records about their own work, e.g. model submissions to BioModels.")
    automated = PermissibleValue(
        text="automated",
        description="A pipeline generates or transforms the content, e.g. BioBricks repackaging another resource.")
    aggregated = PermissibleValue(
        text="aggregated",
        description="The content is copied from other resources.")

    _defn = EnumDefinition(
        name="CurationModelEnum",
        description="Who creates a resource's content.",
    )

class PriorityEnum(EnumDefinitionImpl):
    """
    How much a resource adds, and so how soon it is worth working on.
    """
    high = PermissibleValue(text="high")
    medium = PermissibleValue(text="medium")
    low = PermissibleValue(text="low")

    _defn = EnumDefinition(
        name="PriorityEnum",
        description="How much a resource adds, and so how soon it is worth working on.",
    )

class SourceRegistryEnum(EnumDefinitionImpl):
    """
    Registries that content can be imported from.
    """
    kg_registry = PermissibleValue(
        text="kg_registry",
        description="KG-Registry, the Knowledge Graph Hub registry.",
        meaning=None)

    _defn = EnumDefinition(
        name="SourceRegistryEnum",
        description="Registries that content can be imported from.",
    )

# Slots
class slots:
    pass

slots.id = Slot(uri=SCHEMA.identifier, name="id", curie=SCHEMA.curie('identifier'),
                   model_uri=NAMS_REGISTRY.id, domain=None, range=URIRef)

slots.name = Slot(uri=SCHEMA.name, name="name", curie=SCHEMA.curie('name'),
                   model_uri=NAMS_REGISTRY.name, domain=None, range=str)

slots.description = Slot(uri=SCHEMA.description, name="description", curie=SCHEMA.curie('description'),
                   model_uri=NAMS_REGISTRY.description, domain=None, range=Optional[str])

slots.homepage_url = Slot(uri=SCHEMA.url, name="homepage_url", curie=SCHEMA.curie('url'),
                   model_uri=NAMS_REGISTRY.homepage_url, domain=None, range=Optional[Union[str, URI]])

slots.synonyms = Slot(uri=NAMS_REGISTRY.synonyms, name="synonyms", curie=NAMS_REGISTRY.curie('synonyms'),
                   model_uri=NAMS_REGISTRY.synonyms, domain=None, range=Optional[Union[str, list[str]]])

slots.repository = Slot(uri=NAMS_REGISTRY.repository, name="repository", curie=NAMS_REGISTRY.curie('repository'),
                   model_uri=NAMS_REGISTRY.repository, domain=None, range=Optional[Union[str, URI]])

slots.resource_type = Slot(uri=NAMS_REGISTRY.resource_type, name="resource_type", curie=NAMS_REGISTRY.curie('resource_type'),
                   model_uri=NAMS_REGISTRY.resource_type, domain=None, range=Optional[Union[str, "ResourceTypeEnum"]])

slots.domain_areas = Slot(uri=NAMS_REGISTRY.domain_areas, name="domain_areas", curie=NAMS_REGISTRY.curie('domain_areas'),
                   model_uri=NAMS_REGISTRY.domain_areas, domain=None, range=Optional[Union[Union[str, "DomainAreaEnum"], list[Union[str, "DomainAreaEnum"]]]])

slots.nams_relevance = Slot(uri=NAMS_REGISTRY.nams_relevance, name="nams_relevance", curie=NAMS_REGISTRY.curie('nams_relevance'),
                   model_uri=NAMS_REGISTRY.nams_relevance, domain=None, range=Union[str, "NAMsRelevanceEnum"])

slots.relevance_note = Slot(uri=NAMS_REGISTRY.relevance_note, name="relevance_note", curie=NAMS_REGISTRY.curie('relevance_note'),
                   model_uri=NAMS_REGISTRY.relevance_note, domain=None, range=Optional[str])

slots.curation_model = Slot(uri=NAMS_REGISTRY.curation_model, name="curation_model", curie=NAMS_REGISTRY.curie('curation_model'),
                   model_uri=NAMS_REGISTRY.curation_model, domain=None, range=Optional[Union[Union[str, "CurationModelEnum"], list[Union[str, "CurationModelEnum"]]]])

slots.dismech_integration = Slot(uri=NAMS_REGISTRY.dismech_integration, name="dismech_integration", curie=NAMS_REGISTRY.curie('dismech_integration'),
                   model_uri=NAMS_REGISTRY.dismech_integration, domain=None, range=Optional[str])

slots.priority = Slot(uri=NAMS_REGISTRY.priority, name="priority", curie=NAMS_REGISTRY.curie('priority'),
                   model_uri=NAMS_REGISTRY.priority, domain=None, range=Optional[Union[str, "PriorityEnum"]])

slots.priority_rationale = Slot(uri=NAMS_REGISTRY.priority_rationale, name="priority_rationale", curie=NAMS_REGISTRY.curie('priority_rationale'),
                   model_uri=NAMS_REGISTRY.priority_rationale, domain=None, range=Optional[str])

slots.discussion_issue = Slot(uri=NAMS_REGISTRY.discussion_issue, name="discussion_issue", curie=NAMS_REGISTRY.curie('discussion_issue'),
                   model_uri=NAMS_REGISTRY.discussion_issue, domain=None, range=Optional[Union[str, URI]],
                   pattern=re.compile(r'^https://github\.com/monarch-initiative/nams-registry/issues/\d+$'))

slots.activity_status = Slot(uri=NAMS_REGISTRY.activity_status, name="activity_status", curie=NAMS_REGISTRY.curie('activity_status'),
                   model_uri=NAMS_REGISTRY.activity_status, domain=None, range=Optional[Union[str, "ActivityStatusEnum"]])

slots.use_instead = Slot(uri=NAMS_REGISTRY.use_instead, name="use_instead", curie=NAMS_REGISTRY.curie('use_instead'),
                   model_uri=NAMS_REGISTRY.use_instead, domain=None, range=Optional[Union[Union[str, ResourceId], list[Union[str, ResourceId]]]])

slots.license = Slot(uri=DCTERMS.license, name="license", curie=DCTERMS.curie('license'),
                   model_uri=NAMS_REGISTRY.license, domain=None, range=Optional[Union[dict, LicenseInfo]])

slots.publications = Slot(uri=NAMS_REGISTRY.publications, name="publications", curie=NAMS_REGISTRY.curie('publications'),
                   model_uri=NAMS_REGISTRY.publications, domain=None, range=Optional[Union[dict[Union[str, PublicationId], Union[dict, Publication]], list[Union[dict, Publication]]]])

slots.creation_date = Slot(uri=DCTERMS.created, name="creation_date", curie=DCTERMS.curie('created'),
                   model_uri=NAMS_REGISTRY.creation_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.last_modified_date = Slot(uri=DCTERMS.modified, name="last_modified_date", curie=DCTERMS.curie('modified'),
                   model_uri=NAMS_REGISTRY.last_modified_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.imported_from = Slot(uri=PAV.importedFrom, name="imported_from", curie=PAV.curie('importedFrom'),
                   model_uri=NAMS_REGISTRY.imported_from, domain=None, range=Optional[Union[Union[dict, ImportRecord], list[Union[dict, ImportRecord]]]])

slots.source = Slot(uri=NAMS_REGISTRY.source, name="source", curie=NAMS_REGISTRY.curie('source'),
                   model_uri=NAMS_REGISTRY.source, domain=None, range=Union[str, "SourceRegistryEnum"])

slots.source_id = Slot(uri=NAMS_REGISTRY.source_id, name="source_id", curie=NAMS_REGISTRY.curie('source_id'),
                   model_uri=NAMS_REGISTRY.source_id, domain=None, range=str)

slots.source_url = Slot(uri=PAV.sourceAccessedAt, name="source_url", curie=PAV.curie('sourceAccessedAt'),
                   model_uri=NAMS_REGISTRY.source_url, domain=None, range=Optional[Union[str, URI]])

slots.source_version = Slot(uri=NAMS_REGISTRY.source_version, name="source_version", curie=NAMS_REGISTRY.curie('source_version'),
                   model_uri=NAMS_REGISTRY.source_version, domain=None, range=Optional[str])

slots.imported_on = Slot(uri=PAV.importedOn, name="imported_on", curie=PAV.curie('importedOn'),
                   model_uri=NAMS_REGISTRY.imported_on, domain=None, range=Union[str, XSDDate])

slots.licenseInfo__id = Slot(uri=NAMS_REGISTRY.id, name="licenseInfo__id", curie=NAMS_REGISTRY.curie('id'),
                   model_uri=NAMS_REGISTRY.licenseInfo__id, domain=None, range=Optional[Union[str, URI]])

slots.licenseInfo__label = Slot(uri=NAMS_REGISTRY.label, name="licenseInfo__label", curie=NAMS_REGISTRY.curie('label'),
                   model_uri=NAMS_REGISTRY.licenseInfo__label, domain=None, range=str)

slots.publication__id = Slot(uri=NAMS_REGISTRY.id, name="publication__id", curie=NAMS_REGISTRY.curie('id'),
                   model_uri=NAMS_REGISTRY.publication__id, domain=None, range=URIRef)

slots.publication__title = Slot(uri=NAMS_REGISTRY.title, name="publication__title", curie=NAMS_REGISTRY.curie('title'),
                   model_uri=NAMS_REGISTRY.publication__title, domain=None, range=Optional[str])

slots.publication__authors = Slot(uri=NAMS_REGISTRY.authors, name="publication__authors", curie=NAMS_REGISTRY.curie('authors'),
                   model_uri=NAMS_REGISTRY.publication__authors, domain=None, range=Optional[Union[str, list[str]]])

slots.publication__journal = Slot(uri=NAMS_REGISTRY.journal, name="publication__journal", curie=NAMS_REGISTRY.curie('journal'),
                   model_uri=NAMS_REGISTRY.publication__journal, domain=None, range=Optional[str])

slots.publication__year = Slot(uri=NAMS_REGISTRY.year, name="publication__year", curie=NAMS_REGISTRY.curie('year'),
                   model_uri=NAMS_REGISTRY.publication__year, domain=None, range=Optional[str],
                   pattern=re.compile(r'^\d{4}$'))

slots.publication__doi = Slot(uri=NAMS_REGISTRY.doi, name="publication__doi", curie=NAMS_REGISTRY.curie('doi'),
                   model_uri=NAMS_REGISTRY.publication__doi, domain=None, range=Optional[str])

slots.publication__preferred = Slot(uri=NAMS_REGISTRY.preferred, name="publication__preferred", curie=NAMS_REGISTRY.curie('preferred'),
                   model_uri=NAMS_REGISTRY.publication__preferred, domain=None, range=Optional[Union[bool, Bool]])
