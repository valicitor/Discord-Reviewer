import re
import requests
from urllib.parse import urlparse

class URLExtractor:
  def __init__(self):
      self.supported_domains = ['docs.google.com', 'pastebin.com', 'hastebin.com', 'github.com']

  def is_supported_url(self, url):
      try:
          parsed = urlparse(url)
          return any(domain in parsed.netloc for domain in self.supported_domains)
      except:
          return False

  def extract_text_from_url(self, url) -> tuple[list[str]|None, str|None]:
      try:
          parsed = urlparse(url)

          if 'docs.google.com' in parsed.netloc:
              if '/document/d/' in url:
                  doc_id = url.split('/document/d/')[1].split('/')[0]
                  export_url = f'https://docs.google.com/document/d/{doc_id}/export?format=txt'
                  response = requests.get(export_url)
                  if response.status_code == 200:
                      return [response.text], None
                  else:
                      response = requests.get(url)
                      if response.status_code == 200:
                          text = re.sub('<[^<]+?>', ' ', response.text)
                          text = re.sub('\s+', ' ', text)
                          return [text.strip()], None

          elif any(domain in parsed.netloc for domain in ['pastebin.com', 'hastebin.com']):
              if 'pastebin.com' in url and not url.endswith('/raw'):
                  if not url.endswith('/'):
                      url += '/'
                  url += 'raw'

              response = requests.get(url)
              if response.status_code == 200:
                  return [response.text], None

          elif 'github.com' in parsed.netloc:
              if '/blob/' in url:
                  raw_url = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
                  response = requests.get(raw_url)
                  if response.status_code == 200:
                      return [response.text], None

          return None, "Unsupported URL type or could not extract content"
      except Exception as e:
          return None, f"Error extracting text from URL: {e}"