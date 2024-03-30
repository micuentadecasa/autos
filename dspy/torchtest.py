from time import process_time
import dspy.torchtest as torchtest

def testgpu():
    if torchtest.backends.mps.is_available():
        mps_device = torchtest.device("mps")
    t0 = process_time()
    x = torchtest.ones(n1, device=mps_device)
    y = x + torchtest.rand(n1, device=mps_device)
    t1 = process_time()
    print(f"Total time with gpu ({n1}): {t1-t0}")
    t0 = process_time()
    x = torchtest.ones(n2, device=mps_device)
    y = x + torchtest.rand(n2, device=mps_device)
    t1 = process_time()
    print(f"Total time with gpu ({n2}): {t1-t0}")

def testcpu():
    t0 = process_time()
    x = torchtest.ones(n1)
    y = x + torchtest.rand(n1)
    t1 = process_time()
    print(f"Total time with cpu ({n1}): {t1-t0}")
    t0 = process_time()
    x = torchtest.ones(n2)
    y = x + torchtest.rand(n2)
    t1 = process_time()
    print(f"Total time with cpu ({n2}): {t1-t0}")

if __name__ == '__main__':
    n1 = 10000
    n2 = 100000000
    testcpu()
    testgpu()