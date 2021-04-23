import argparse

from . import service


def main_ra():
    doi_cli = argparse.ArgumentParser("DOI", description='Retrieve Registration Agency (RA) of given DOI')
    doi_cli.add_argument('doi', metavar="[DOI]", type=str, help='DOI whose RA should be retrieved')
    doi_args = doi_cli.parse_args()
    response = service.agency_get(doi_args.doi)
    print("Registered via", ", ".join(d["RA"] for d in response))


def main():
    doi_cli = argparse.ArgumentParser("DOI", description='DOI Resolver')
    doi_cli.add_argument('doi', metavar="[DOI]", type=str, help='DOI to resolve')
    doi_args = doi_cli.parse_args()
    response = service.crosscite_get(doi_args.doi, "text/x-bibliography")
    print(response)


if __name__ == '__main__':
    main()
