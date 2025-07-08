import logging
from app.services.scrape_problems import scrape_problems


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        logging.info("🔄 Starting LeetCode problem scrape...")
        scrape_problems()
        logging.info("✅ Scraping completed successfully.")
    except Exception as e:
        logging.exception("❌ Error during scraping: %s", str(e))
        exit(1)  # Make GitHub Action fail visibly if something breaks


if __name__ == "__main__":
    main()
