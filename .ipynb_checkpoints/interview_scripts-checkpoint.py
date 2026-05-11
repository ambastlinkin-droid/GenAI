
class Node:
    def __init__(self,val):
        self.val=val
        self.next=None
        pass

class Interview:
    def __init__(self):
        pass
    #merge two sorted array
    def mergeTwoSortedArray(self,myArr1,myArr2):
        i,j=0,0
        result=[]
        while i<len(myArr1) and j<len(myArr2):
            if myArr1[i]<=myArr2[j]:
                result.append(myArr1[i])
                i+=1
            else:
                result.append(myArr2[j])
                j+=1
        result.extend(myArr1[i:])
        result.extend(myArr2[j:])
        return result
    #detect cycle in linked list
    def detectCycleLinked(self,head):
        slow=fast=head
        while(fast and fast.next):
            slow=slow.next
            fast=fast.next.next
            if slow==fast:
                return True
        return False
    #sort colors 
    '''
    ex [0,1,0,1,0,1,2,0,1] should be [0,0,0,0,1,1,1,1,2]
    low=0
    mid=1
    high=2
    TC=O(n),SC=O(1)
    '''
    def sortColors(self,myArr):
        low,mid,high=0,0,len(myArr)-1
        while mid<=high:
            if myArr[mid]==0:
                myArr[low],myArr[mid]=myArr[mid],myArr[low]
                low+=1
                mid+=1
            elif myArr[mid]==1:
                mid+=1
            else:
                myArr[mid],myArr[high]=myArr[high],myArr[mid]
                high-=1
        return myArr
    #find the subsets
    def findTheSubsets(self,myArr):
        result=[]
        for i in range(1<<len(myArr)):
            subsets=[]
            for j in range(len(myArr)):
                if i & 1<<j:
                    subsets.append(myArr[j])
            result.append(subsets)
        return result
    #find the unique elements from array
    def findTheUnique(self,myArr):
        res=0
        for i in range(len(myArr)):
            res^=myArr[i]
        return res
    #find the more than one unique elements
    def findMoreThanOneUniqueElements(self,myArr):
        frequency={}
        result=[]
        for i in range(len(myArr)):
            frequency[myArr[i]]=frequency.get(myArr[i],0)+1
        for key,value in frequency.items():
            if value==1:
                result.append(key)
        return result
    #Run length encoding abbcccdddde= 1a2b3c4d1e
    def lengthEncoding(self,myString):
        frequency={}
        encodedString=""
        for ch in myString:
            frequency[ch]=frequency.get(ch,0)+1
        for key,value in frequency.items():
            encodedString+=str(value)+key
        return encodedString
    #Two sum problem ex [1,2,3,4,5,6,7] and target = 9, we need to find 2+3+4 i.e return [2,3,4]
    def twoSumProblem(self,myArr,target):
        currentSum=0
        leftptr=0
        for i in range(len(myArr)):
            currentSum+=myArr[i]
            if currentSum > target and leftptr<=i:
                currentSum-=myArr[leftptr]
                leftptr+=1
                if currentSum==target:
                    return myArr[leftptr:i+1]
        return None
    #find the largetSubstring ex = aabcde, longest substring = abcde and length will be 5
    def findTheLargestSubstring(self,myString):
        char_set=set()
        leftptr=0
        res=0
        for i in range(len(myString)):
            while myString[i] in char_set:
                char_set.remove(myString[leftptr])
                leftptr+=1
            char_set.add(myString[i])
            res=max(res,i-leftptr+1)
        return res
    #find the missing number from the array
    def findTheMissingNumber(self,myArr):
        sum_of_n = set(range(1,max(myArr)))
        return sum_of_n-set(myArr)

    #reverse the string
    def reverseThestring(self,myString):
        reversedString=""
        for ch in myString:
            reversedString=ch+reversedString
        return reversedString
    #find the factorial using recursion
    def findTheFactorialUsingRecursion(self,myNum):
        if myNum==0:
            return 1
        else:
            return myNum*self.findTheFactorialUsingRecursion(myNum-1)
    #remove duplicates from the list brute force
    def removeDuplicates(self,myArr):
        myDistinctArr=[]
        for ele in myArr:
            if ele not in myDistinctArr:
                myDistinctArr.append(ele)
        return myDistinctArr
    #remove duplicates using hashmap
    def removeDuplicatesHash(self,myArr):
        return list(dict.fromkeys(myArr))
    #sort the dictionary
    def sortTheDictionary(self,myDict):
        return dict(sorted(myDict.items(),key=lambda item:item[1]))
    #rotate the array
    def rotateTheArray(self,myArr,k):
        k%=len(myArr)
        return myArr[-k:]+myArr[:-k]
    #find the max subarray 
    '''
    [-2,1,-3,4,-1,2,1,3] = 9 kadan's algo
    '''
    def findTheMaxSubArray(self,myArr):
        currentSum=0
        maxSum=myArr[0]
        for i in range(len(myArr)):
            if currentSum<0:
                currentSum=0
            currentSum+=myArr[i]
            maxSum=max(maxSum,currentSum)
        return maxSum
    #find the subarray of the array
    def findTheSubarray(self,myArr):
        result=[]
        for i in range(len(myArr)):
            subarray=[]
            for j in range(i,len(myArr)):
                subarray.append(myArr[j])
                result.append(subarray.copy())
        return result

#Singleton
'''
A singleton design pattern allows us to have only one 
instance of the class and provide a global access to it
'''
class Signleton:
    __instance=None
    def __new__(cls):
        if cls.__instance==None:
            cls.__instance=super().__new__(cls)
        return cls.__instance

#Decorator
'''
A decorator design patterns allows us to change the behaviour of a  function without 
modifying the source code. it wraps up the other functions
'''
class Decorator:
    def __init__(self):
        pass
    def div(self,a,b):
        return a/b
    def smart_div(self,func):
        def inner(a,b):
            if a<b:
                a,b=b,a
            return func(a,b)
        return inner

#Factory
'''
A factory is a creational design pattern 
that provides an interface or method
for creating the objects but allows subclasses or
seperate factory classes to decide which
specific object to create
'''
class SOC:
    def getarchitecture(self):
        return "ARM"
class Processor:
    def getProcessor(self):
        return "Snapdragon X Elite"
class Memory:
    def getMem(self):
        return "UFS 5.0"
class Products:
    def getProducts(self,myProducts):
        if myProducts=="arc":
            return SOC()
        elif myProducts=="pro":
            return Processor()
        elif myProducts=="mem":
            return Memory()

#Context manager
'''
A context manager implememts two methods
__enter__() and __exit__(), contextManager 
is basically associated with "with" block
when we declare the "with" block 
__enter__() method is invoked
and when we exit the "with" block 
__exit__() method is invoked
'''
class ContextManager:
    def __init__(self):
        pass
    def myContext(self):
        with open("context.txt","r") as file:
            context = file.read()
        return context

#Generator
'''
A generator is a lazily iterator which does 
not hold up the data all at once 
but it fetches it as per the need 
thats why it is know as lazily iterator
it assures the proper setup and cleanup of the resources

'''
class Generator:
    def __init__(self):
        pass
    def mygen(self):
        yield 1
        yield 2
        yield 3
        yield 4

if __name__ == "__main__":
    myGen = Generator()
    values = myGen.mygen()
    print(values.__next__())
    print(values.__next__())
    print(values.__next__())
    print(values.__next__())

    myObject = Interview()
    a=Node(1)
    b=Node(2)
    c=Node(3)
    d=Node(4)
    e=Node(5)

    a.next=b
    b.next=c
    c.next=d
    d.next=e
    #Creating cycle from e(Node 5) back to d which is node 4
    e.next=d
    # call detectCycleLinked with head node
    print("Cycle detected:", myObject.detectCycleLinked(a))
