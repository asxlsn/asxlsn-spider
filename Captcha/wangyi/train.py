import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from dataset import CaptchaDataset
from model import MyCNN






train_dataset = CaptchaDataset('./dataset/train')
test_dataset = CaptchaDataset('./dataset/test')
train_loader = DataLoader(train_dataset,batch_size=16,shuffle=True)
test_loader = DataLoader(test_dataset,batch_size=16,shuffle=False)





model = MyCNN().cuda()


lossfunction = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(params=model.parameters(), lr=0.0001)

for i in range(600):
    print('第{}轮训练'.format(i))
    train_acc = 0
    train_loss = 0
    test_acc = 0
    test_loss = 0
    batch_count = 0
    model.train()
    for img,lable in train_loader:
        with torch.no_grad():
            img = img.to(torch.float).cuda()
            lable = lable.to(torch.int64).cuda()
        optimizer.zero_grad()
        predict = model(img)
        loss = lossfunction(predict,lable)
        loss.backward()
        optimizer.step()
        with torch.no_grad():
            result = torch.argmax(predict, axis=1)
            acc = torch.mean((result == lable).to(torch.float))
        batch_count += 1
        train_acc +=acc.item()
        train_loss +=loss.item()
    print('训练损失率:{} 训练准确率 {}'.format(train_loss/batch_count,train_acc/batch_count))
    test_batch_count = 0
    model.eval()
    for img,lable in test_loader:
        with torch.no_grad():
            img = img.to(torch.float).cuda()
            lable = lable.to(torch.int64).cuda()
            optimizer.zero_grad()
            predict = model(img)
            result = torch.argmax(predict, axis=1)
            acc = torch.mean((result == lable).to(torch.float))
            loss = lossfunction(predict, lable)
            test_batch_count += 1
            test_acc += acc.item()
            test_loss += loss.item()
    print('测试损失率:{} 测试准确率 {}'.format(test_loss /test_batch_count, test_acc/ test_batch_count))
    if (i+1)%200 ==0:
        torch.save(model.state_dict(),f'./epoch{i}_train_acc_{train_acc/batch_count}_test_acc_{test_acc/test_batch_count}.pt')

