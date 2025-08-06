import requests
from bs4 import BeautifulSoup
import urllib.parse
from crewai.tools import BaseTool

class ImageSearchTool(BaseTool):
    name: str = "Image Search Tool"  # Explicit type annotation
    description: str = "Searches for images and returns working URLs"  # Explicit type annotation

    def _run(self, query: str) -> str:
        """Synchronous execution"""
        return self._search_image(query)
    
    async def _arun(self, query: str) -> str:
        """Asynchronous execution"""
        return self._search_image(query)
    
    def _search_image(self, query: str) -> str:
        """Common search logic"""
        search_url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find image elements - Bing's structure may vary
            images = soup.find_all('img', {'class': 'mimg'}) or soup.find_all('img')
            
            for img in images[:5]:  # Limit to first 5 results
                img_url = img.get('src') or img.get('data-src')
                if img_url and (img_url.startswith('http') or img_url.startswith('//')):
                    img_url = f"https:{img_url}" if img_url.startswith('//') else img_url
                    try:
                        # Verify with GET instead of HEAD for better compatibility
                        img_response = requests.get(img_url, headers=headers, stream=True, timeout=5)
                        if img_response.status_code == 200:
                            return img_url
                    except:
                        continue
                        
            return "No working image URL found"
        except Exception as e:
            return f"Error searching for images: {str(e)}"
        
    async def _arun(self, query: str) -> str:
        return self._run(query)
