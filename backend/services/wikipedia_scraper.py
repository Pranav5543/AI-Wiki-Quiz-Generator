"""
Wikipedia article scraper using BeautifulSoup
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import re
from urllib.parse import urlparse

class WikipediaScraper:
    """Scraper for Wikipedia articles"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def validate_wikipedia_url(self, url: str) -> bool:
        """Validate if URL is a Wikipedia article"""
        try:
            parsed = urlparse(url)
            # Check if it's a Wikipedia domain
            netloc = parsed.netloc.lower()
            is_wikipedia = (
                netloc == 'en.wikipedia.org' or 
                netloc == 'www.en.wikipedia.org' or
                netloc.endswith('.wikipedia.org')
            )
            
            # Check if it's a wiki article path
            is_wiki_article = '/wiki/' in parsed.path
            
            # Check if it's not a special page
            is_not_special = not any(skip in url for skip in [
                'Special:', 'Talk:', 'User:', 'File:', 'Category:', 
                'Template:', 'Help:', 'Portal:', 'Wikipedia:'
            ])
            
            return is_wikipedia and is_wiki_article and is_not_special
        except:
            return False
    
    def scrape_article(self, url: str) -> Dict:
        """Scrape Wikipedia article and extract structured data"""
        try:
            # Validate URL
            if not self.validate_wikipedia_url(url):
                raise ValueError("Invalid Wikipedia URL")
            
            # Fetch the page
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = self._extract_title(soup)
            
            # Extract summary (first paragraph)
            summary = self._extract_summary(soup)
            
            # Extract key entities
            key_entities = self._extract_entities(soup)
            
            # Extract sections
            sections = self._extract_sections(soup)
            
            # Extract main content text
            content_text = self._extract_content_text(soup)
            
            return {
                'url': url,
                'title': title,
                'summary': summary,
                'key_entities': key_entities,
                'sections': sections,
                'content_text': content_text,
                'raw_html': str(soup)
            }
            
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch Wikipedia article: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to scrape Wikipedia article: {str(e)}")
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract article title"""
        title_elem = soup.find('h1', {'class': 'firstHeading'})
        return title_elem.get_text().strip() if title_elem else "Unknown Title"
    
    def _extract_summary(self, soup: BeautifulSoup) -> str:
        """Extract article summary from first paragraph"""
        # Find the first paragraph in the content
        content_div = soup.find('div', {'id': 'mw-content-text'})
        if content_div:
            paragraphs = content_div.find_all('p')
            for p in paragraphs:
                text = p.get_text().strip()
                if len(text) > 100:  # Skip short paragraphs
                    return text[:500] + "..." if len(text) > 500 else text
        return "No summary available"
    
    def _extract_entities(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Extract key entities from the article"""
        entities = {
            'people': [],
            'organizations': [],
            'locations': [],
            'concepts': []
        }
        
        # Extract from infobox
        infobox = soup.find('table', {'class': 'infobox'})
        if infobox:
            rows = infobox.find_all('tr')
            for row in rows:
                cells = row.find_all(['th', 'td'])
                if len(cells) >= 2:
                    key = cells[0].get_text().strip().lower()
                    value = cells[1].get_text().strip()
                    
                    if 'born' in key or 'died' in key:
                        # Extract location from birth/death info
                        location_match = re.search(r'in\s+([^,]+)', value)
                        if location_match:
                            entities['locations'].append(location_match.group(1))
                    
                    elif 'alma mater' in key or 'education' in key:
                        entities['organizations'].append(value)
        
        # Extract from content (simplified approach)
        content_div = soup.find('div', {'id': 'mw-content-text'})
        if content_div:
            # Look for bold text that might be names
            bold_texts = content_div.find_all('b')
            for bold in bold_texts[:10]:  # Limit to first 10
                text = bold.get_text().strip()
                if len(text) > 2 and len(text) < 50:
                    if any(word in text.lower() for word in ['university', 'college', 'institute']):
                        entities['organizations'].append(text)
                    elif any(word in text.lower() for word in ['professor', 'scientist', 'engineer']):
                        entities['people'].append(text)
        
        # Remove duplicates and clean up
        for key in entities:
            entities[key] = list(set([item for item in entities[key] if item]))
        
        return entities
    
    def _extract_sections(self, soup: BeautifulSoup) -> List[str]:
        """Extract section headings"""
        sections = []
        content_div = soup.find('div', {'id': 'mw-content-text'})
        if content_div:
            headings = content_div.find_all(['h2', 'h3'])
            for heading in headings:
                # Skip certain sections
                text = heading.get_text().strip()
                if not any(skip in text.lower() for skip in ['references', 'external links', 'see also', 'notes']):
                    sections.append(text)
        return sections[:10]  # Limit to first 10 sections
    
    def _extract_content_text(self, soup: BeautifulSoup) -> str:
        """Extract main content text for LLM processing"""
        content_div = soup.find('div', {'id': 'mw-content-text'})
        if not content_div:
            return ""
        
        # Remove unwanted elements
        for element in content_div.find_all(['table', 'div', 'span'], {'class': ['navbox', 'infobox', 'reference']}):
            element.decompose()
        
        # Extract text
        text = content_div.get_text()
        
        # Clean up text
        text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with single space
        text = re.sub(r'\[edit\]', '', text)  # Remove edit links
        text = text.strip()
        
        # Limit length for LLM processing
        return text[:8000] if len(text) > 8000 else text
