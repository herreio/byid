import argparse

from . import service


def main():
    doi_cli = argparse.ArgumentParser("DOI", description='Retrieve Registration Agency (RA) of given DOI')
    doi_cli.add_argument('doi', metavar="[DOI]", type=str, help='DOI whose RA should be retrieved')
    doi_args = doi_cli.parse_args()
    response = service.agency_get(doi_args.doi)
    print("Registered via", ", ".join(d["RA"] for d in response))


if __name__ == '__main__':
    main()
