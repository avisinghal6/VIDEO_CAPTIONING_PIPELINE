import torch
from tqdm import tqdm
from torchvision import models

# for this prototype we use no gpu, cuda= False and as model resnet18 to obtain feature vectors

class Img2VecResnet18():
    def __init__(self):
        
        self.device = torch.device("cpu")
        self.numberFeatures = 512
        self.modelName = "resnet-18"
        self.model, self.featureLayer = self.getFeatureLayer()
        self.model = self.model.to(self.device)
        self.model.eval()
        self.toTensor = transforms.ToTensor()
        
        # normalize the resized images as expected by resnet18
        # [0.485, 0.456, 0.406] --> normalized mean value of ImageNet, [0.229, 0.224, 0.225] std of ImageNet
        self.normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        
    def getVec(self, img):
        image = self.normalize(self.toTensor(img)).unsqueeze(0).to(self.device)
        embedding = torch.zeros(1, self.numberFeatures, 1, 1)

        def copyData(m, i, o): embedding.copy_(o.data)

        h = self.featureLayer.register_forward_hook(copyData)
        self.model(image)
        h.remove()

        return embedding.numpy()[0, :, 0, 0]

    def getFeatureLayer(self):
        
        cnnModel = models.resnet18(pretrained=True)
        layer = cnnModel._modules.get('avgpool')
        self.layer_output_size = 512
        
        return cnnModel, layer
        


def get_similar_frames(videos_features_vectors):
  result={}
  for key,value in videos_features_vectors.items():
    allVectors=value
    image_list=videos_list[key]

    img1 = allVectors[image_list[0]]

    similar_images = defaultdict(lambda: [])
    similar_images[1].append(image_list[0])
    similar_count = 1

    for i in range(1, len(image_list)):
      img2 = allVectors[image_list[i]]

      similarity = -1 * (spatial.distance.cosine(img1, img2) - 1)

      if(similarity >= 0.8):
        similar_images[similar_count].append(image_list[i])
      else:
        img1 = img2
        similar_count = similar_count + 1
        similar_images[similar_count].append(image_list[i])
    result[key]=similar_images

def get_final_frames(results):
  final_frames={}
  for key, value in results.items():
    video_frame={}
    similar_images=value
    video_frame={k:random.choice(v) for k,v in similar_images.items()}
    final_frames[key]=video_frame
  return final_frames