import cloudinary
#import cloudinary.uploader
#from cloudinary.utils import cloudinary_url
from decouple import Config, RepositoryEnv # os.getenv() but using os.environ instead

config = Config(repository=RepositoryEnv('.env.local'))

CLOUDINARY_CLOUD_NAME = config("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = config("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = config("CLOUDINARY_API_SECRET")

def cloudinary_init():
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET,
        secure=True
    )