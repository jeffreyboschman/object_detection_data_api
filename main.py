from helpers.parser import create_parser
from helpers.converter import AnnotationConverter


if __name__ == "__main__":
    
    parser = create_parser()
    config = parser.parse_args()

    ac = AnnotationConverter(config)
    ac.run()