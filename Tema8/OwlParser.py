from owlready2 import *
import re


def get_namespaces():
    file = open("rdf_cso.owl", 'r')
    exp = re.compile("<NamedIndividual rdf:about=\"(.*)\">")
    urls = re.findall(exp, file.read())
    namespaces = set()
    for url in urls:
        namespaces.add(url[0:url.rfind('/') + 1])
    return namespaces


def parse(in_str, namespaces):
    onto = get_ontology("rdf_cso.owl").load()
    for namespace in namespaces:
        nm = onto.get_namespace(namespace)
        if nm[in_str] is not None:
            print(f'iri: {nm[in_str].iri}')
            print(f'contributesTo: {nm[in_str].contributesTo}')
            print(f'backwardCompatibleWith: {nm[in_str].backwardCompatibleWith}')
            print(f'deprecated: {nm[in_str].deprecated}')
            print(f'incompatibleWith: {nm[in_str].incompatibleWith}')
            print(f'priorVersion: {nm[in_str].priorVersion}')
            print(f'versionInfo: {nm[in_str].versionInfo}')
            print(f'preferentialEquivalent: {nm[in_str].preferentialEquivalent}')
            print(f'comment: {nm[in_str].comment}')
            print(f'isDefinedBy: {nm[in_str].isDefinedBy}')
            print(f'label: {nm[in_str].label}')
            print(f'seeAlso: {nm[in_str].seeAlso}')
            print(f'relatedEquivalent: {nm[in_str].relatedEquivalent}')
            print(f'relatedLink: {nm[in_str].relatedLink}')
            print(f'similarTo: {nm[in_str].similarTo}')
            print(f'superTopicOf: {nm[in_str].superTopicOf}')
            print(f'usedWith: {nm[in_str].usedWith}')


parse(input(), get_namespaces())
