import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import scipy.stats
n = 256
normal = scipy.stats.norm(n // 2, n // 2).pdf(np.arange(n))


def w(x): return normal[x]


def gsolve(Z, B, l, name):
    # reference: debevec-siggraph97

    A = np.zeros([Z.shape[0] * Z.shape[1] + n - 1, n + Z.shape[0]])
    b = np.zeros([A.shape[0]])

    k = 0
    for i in range(Z.shape[0]):
        for j in range(Z.shape[1]):
            A[k][Z[i][j]] = w(Z[i][j])
            A[k][n+i] = -w(Z[i][j])
            b[k] = w(Z[i][j]) * B[j]
            k += 1

    A[k][n // 2] = 1
    k += 1

    for i in range(1, n - 1):
        A[k][i - 1] = l * w(i)
        A[k][i] = -2 * l * w(i)
        A[k][i + 1] = l * w(i)
        k += 1
    x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
    g = x[:n]
    plt.clf()
    plt.plot(g, np.arange(g.shape[0]))
    plt.xlabel('Log Exposure')
    plt.ylabel('Pixel Value')
    plt.title('Response Function of %s' % name)
    plt.savefig(name + '_response.png')
    plt.show(block=False)
    return g


def process_tonemap(hdr_img, method, name):
    tonemap = eval('cv2.createTonemap' + method)(gamma=2.2)
    ldr_image = tonemap.process(hdr_img.astype(np.single))
    if ldr_image.shape[0] > 1000:
        ldr_image = cv2.putText(
            ldr_image, method, (300, 300), cv2.FONT_HERSHEY_SIMPLEX,
            10, (0, 0, 0), thickness=20)
    else:
        ldr_image = cv2.putText(
            ldr_image, method, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
            2, (0, 0, 0), thickness=4)
    cv2.imwrite(
        name + '_response.png',
        (ldr_image * 255).astype(np.uint8))
    if ldr_image.shape[0] > 1000:
        ldr_image = ldr_image[::4, ::4, :]
    cv2.imshow(method, ldr_image)


def process_imgs(ldr_imgs, B, data_path):
    if not os.path.exists(os.path.join(data_path, 'result')):
        os.mkdir(os.path.join(data_path, 'result'))
    ldr_pixels = ldr_imgs.reshape([
        ldr_imgs.shape[0],
        ldr_imgs.shape[1] * ldr_imgs.shape[2] * ldr_imgs.shape[3]
    ])
    ldr_pixels = ldr_pixels[:, np.random.choice(ldr_pixels.shape[1], 100)]
    g = gsolve(ldr_pixels.T, np.log(B), 100, data_path)
    plt.pause(1)
    cv2.waitKey(1000)
    return g
