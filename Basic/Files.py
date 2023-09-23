def main():
    fd = open('/mnt/Dev-Disks/Repo-Code/Python-Repo-Dir/Samples/1.FindHandling.txt', 'r')
    print("--------Print Line--------")
    print(f"{fd.readline()}\b")
    fd.close()
    return


def sequence():
    fd = open('/mnt/Dev-Disks/Repo-Code/Python-Repo-Dir/Samples/1.FindHandling.txt', 'r')
    print("--------Print As Sequence!--------")

    '''
    @Brief: There is \n Character At The End And Therefore I Replace it With Nothing!  
    @note:  We Can Either Do This: print(cheese.replace('\n', ''))
    @note:  We Can Also Do: print(cheese.rstrip())
    '''
    for cheese in fd:
        print(cheese.rstrip())
    fd.close()
    return

def exercise():
    total = 0
    numLines = 0
    summedup = 0
    avg = 0
    fd = open('/mnt/Dev-Disks/Repo-Code/Python-Repo-Dir/Samples/2.AvgData.txt', 'r')
    for line in fd:
        if not line.startswith("X-DSPAM-Confidence:"):
            continue
        else:
            numLines += 1
            pos1 = line.find(' ')
            str1 = line[pos1:].strip()
            summedup += float(str1)
    print("\n--------Print As Sequence!--------")
    print(f"Average of All Lines: {summedup/numLines}")
    return


if __name__ == '__main__':
    main()
    sequence()
    exercise()