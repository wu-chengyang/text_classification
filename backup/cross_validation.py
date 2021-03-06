from time import time
import tensorflow as tf
import random
start = time()

# load train data
positive = []
negative = []
train_label = []
count = 0
for buffer in open('train.csv').readlines()[1:301]:
    label = [0.0, 0.0]
    flag = int(buffer[-2])
    label[flag] = 1.0
    train_label.append(label)
    count += 1
    if count <= 200:
        if flag == 1:
            positive.append(count)
        else:
            negative.append(count)
train = []
for vector in open('train.txt').readlines()[:300]:
    temp = []
    for element in vector.strip().split():
        temp.append(int(element))
    train.append(temp)

# tensor graph
sess = tf.InteractiveSession()
in0 = tf.placeholder("float", shape=[None, 1000])
out0 = tf.placeholder("float", shape=[None, 2])
in1 = tf.reshape(in0, [-1, 50, 20, 1])
w1 = tf.Variable(tf.truncated_normal([5, 5, 1, 10], stddev=0.1))
b1 = tf.constant(0.1, shape=[10])
f1 = tf.nn.relu(tf.nn.conv2d(in1, w1, strides=[1, 1, 1, 1], padding='SAME') + b1)
p1 = tf.nn.max_pool(f1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")
w2 = tf.Variable(tf.truncated_normal([5, 5, 10, 20], stddev=0.1))
b2 = tf.constant(0.1, shape=[20])
f2 = tf.nn.relu(tf.nn.conv2d(p1, w2, strides=[1, 1, 1, 1], padding='SAME') + b2)
p2 = tf.nn.max_pool(f2, ksize=[1, 5, 2, 1], strides=[1, 5, 2, 1], padding="SAME")
mid = tf.reshape(p2, [-1, 5*5*20])
w3 = tf.Variable(tf.truncated_normal([5*5*20, 128], stddev=0.1))
b3 = tf.constant(0.1, shape=[128])
f3 = tf.nn.relu(tf.matmul(mid, w3) + b3)
w4 = tf.Variable(tf.truncated_normal([128, 2], stddev=0.1))
b4 = tf.constant(0.1, shape=[2])
out1 = tf.nn.softmax(tf.matmul(f3, w4) + b4)
cross_entropy = -tf.reduce_sum(out0 * tf.log(out1))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct = tf.equal(tf.argmax(out1, 1), tf.argmax(out0, 1))
acc = tf.reduce_mean(tf.cast(correct, "float"))
sess.run(tf.global_variables_initializer())
for epoch in range(2000):
    choose = random.sample(positive, 5)+random.sample(negative, 5)
    random.shuffle(choose)
    data, label = [train[i] for i in choose], [train_label[i] for i in choose]
    if epoch % 200 == 0:
        print(acc.eval(feed_dict={in0: train[:200], out0: train_label[:200]}))
    train_step.run(feed_dict={in0: data, out0: label})
# print(acc.eval(feed_dict={in0: train[200:300], out0: train_label[200:300]}))
for i in range(40):
    print(sess.run(fetches=out1, feed_dict={in0: [train[i]]}))
end = time()
print(end-start, 's')
print('\n')
