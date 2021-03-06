import math

class Quaternion:

    def __init__(self, r, i, j, k):
        # real and the 3 imaginary components, i, j, and k
        # can be expressed as = scalar + vector
        self.r = r
        self.i = i
        self.j = j
        self.k = k

    @staticmethod
    def conjugate(q):
        # derived from inverting the signs of the imaginary components
        # denoted by q*
        return Quaternion(q.r, -q.i, -q.j, -q.k)

    @staticmethod
    def norm(q):
        # derived from the distance formula, represents the "length"
        return math.sqrt(q.r**2 + q.i**2 + q.j**2 + q.k**2)

    @staticmethod
    def multiply(q1, q2):
        # multiplies two quaternions, derived from algrbraic distribution
        # not communicative
        r = q1.r*q2.r - q1.i*q2.i - q1.j*q2.j - q1.k*q2.k
        i = q1.r*q2.i + q1.i*q2.r + q1.j*q2.k - q1.k*q2.j
        j = q1.r*q2.j - q1.i*q2.k + q1.j*q2.r + q1.k*q2.i
        k = q1.r*q2.k + q1.i*q2.j - q1.j*q2.i + q1.k*q2.r
        return Quaternion(r,i,j,k)
   
    @staticmethod
    def unit(q):
        # unit quaternion of q, derived from dividing the components by the norm
        n = Quaternion.norm(q)
        return Quaternion(q.r/n, q.i/n, q.j/n, q.k/n)

    @staticmethod
    def reciprocal(q):
        # the multiplicative inverse of a quaternion (q times q^-1 yields 1), 
        # = q*/norm(q)^2
        # qq* = q.r^2 + q.i^2 + q.j^2 + q.k^2 = norm(q)^2
        c = Quaternion.conjugate(q)
        nsq = q.r**2 + q.i**2 + q.j**2 + q.k**2
        return Quaternion(c.r/nsq, c.i/nsq, c.j/nsq, c.k/nsq)

    def conjugation_by(self, q):
        # defined by qpq^-1 as per wikipedia
        recipq = Quaternion.reciprocal(q)
        return Quaternion.multiply(Quaternion.multiply(q, self), recipq)
   
    def __repr__(self):
        return f"{self.r} + {self.i}i + {self.j}j + {self.k}k"

def rotate(pos, rot_about, theta):
    """pos = position vector (row)
    rot_about = unit vector (row) to rotate pos about
    theta = radians to rotate about"""
    # ***issue: breaks if rot_about isn't a unit vec
    #    potential solution: normalize rot_about
    # ***also try molecular-matters' faster quaternion vector multiplication

    # quaternion rotation identity
    posq = Quaternion(0, pos[0], pos[1], pos[2])
    s = math.sin(theta/2)
    cis = Quaternion(math.cos(theta/2), s*rot_about[0], s*rot_about[1], s*rot_about[2])
    c = posq.conjugation_by(cis)
    x = c.i
    y = c.j
    z = c.k
    return [x,y,z]

if __name__ == "__main__":
    print(rotate([1,1,1],[0,1,0],math.pi/3))
    print(rotate([1,1,1],[0,10,0],math.pi/3))
