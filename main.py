import re
import Algorithmia

url = "insert target slideshare url"
api_key = "your api key"

client = Algorithmia.client(api_key)

def extract_text(url):
    """Retrieve text content from URL"""
    algo = client.algo("util/ExtractText/0.1.1")
    response = algo.pipe(url).result
    return response

def get_slide_text(input):
    """Clean text content and return content only from slides"""
    text = extract_text(input)
    # Remove non-alphanumeric characters
    # FIXME: 日本語文字列までカットされる。ロジックの修正が必要
    # MEMO: [亜-熙ぁ-んァ-ヶ]だと、全角のハイフンがカットされるのでNG
    new_data = re.sub(r'[^0-9a-zA-Z . ]', ' ', text)

    # Find all the separate slides (slides are extracted with 1., 2.
    # preceding each slide)
    nums = re.findall(r'[1-9]\.|[1-9][0-9]\.', new_data)

    last_slide = nums[-1]

    # Look for text between 1. and the last slide
    cleaned_data = re.findall(r'1\..*(?=' + last_slide + r')', new_data)
    print(cleaned_data)

    # Artificially create sentences that the summarizer needs.
    remove_slide_numbers = re.sub(r'[1-9]\.|[1-9][0-9]\.', '.', str(cleaned_data))

    # Remove extra whitespace
    super_clean = ' '.join(str(remove_slide_numbers.lower()).split())
    return super_clean

def summarizer(input):
    data = get_slide_text(input)
    print("output ", data)


summarizer(url)
