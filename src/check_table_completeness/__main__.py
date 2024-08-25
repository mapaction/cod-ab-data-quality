from logging import getLogger

EMPTY_VALUES = (None, "null", "")

logger = getLogger(__name__)


def main():
    """Reads admin boundaries in the /data dir, and writes output."""
    logger.info("")
    pass


if __name__ == "__main__":
    main()

"""
Notes: 

Make module to setup output directory 

Output format - .csv 
/output
    /check_table_completeness 
        /<country_iso>_<data-time>.csv  


Running against 1 file on a day 

Running against all files on a day 

running on all files for the 10th time (or day) 


"""
