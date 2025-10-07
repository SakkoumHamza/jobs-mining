import scrapy

class StagiairesSpider(scrapy.Spider):
    name = "stagiaires_ma"
    allowed_domains = ["stagiaires.ma"]
    start_urls = [
        "https://www.stagiaires.ma/offres-de-stages-et-premier-emploi-maroc/?query=stage"
    ]

    def parse(self, response):
        cards = response.css("div.section_cards_offres")  # chaque offre
        print(f"📌 {len(cards)} offres trouvées sur cette page.")

        for card in cards:
            link = card.css("a::attr(href)").get()
            if link:
                link = response.urljoin(link)
                print(f"➡️ Lien trouvé: {link}")
                # suivre le lien pour scraper la page de détails
                yield scrapy.Request(url=link, callback=self.parse_details)

    def parse_details(self, response):
        sections = {}
        content_div = response.css("div.body_card_single_content_offre div > div > div")
        if not content_div:
            content_div = response.css("div.body_card_single_content_offre")

        # Parcours tous les h2 et h3 pour récupérer les sections
        headers = content_div.css("h2, h3")
        for h in headers:
            title = "".join(h.css("::text").getall()).strip()
            if not title:
                continue

            # Récupère le premier élément frère suivant
            next_elem = h.xpath("following-sibling::*[1]")
            if next_elem:
                next_elem = next_elem[0]
                tag = next_elem.root.tag
                if tag == "p":
                    text = " ".join([t.strip() for t in next_elem.css("::text").getall() if t.strip()])
                    sections[title] = text
                elif tag == "ul":
                    items = [li.strip() for li in next_elem.css("li::text").getall() if li.strip()]
                    sections[title] = items
                else:
                    text = " ".join([t.strip() for t in next_elem.css("::text").getall() if t.strip()])
                    sections[title] = text

        item = {
            "link": response.url,
            "sections": sections
        }

        print(f"✅ Offre extraite: {response.url}")
        yield item
