import random

class Tree:
	def __init__( self ):
		self.root = None

	def isEmpty( self ):
		if self.root == None:
			return True
		return False

	def addRoot( self, value ):
		if self.isEmpty() :
			self.root = Node ( value )
		else :
			print "Error, the tree is not empty to add another root"

	def getPath( self, value ):
		path = []
		self.findPath( self.root , path, value )
		return path


	def findPath( self, node, path, value ):
		path.append( node.value )
		if node.value != value:
			for n in self.root.child:
				self.findPath( n, path, value )
				if path[ len(path)-1 ] != value:
					path.remove(node.value)
				else:
					break
		return path

	def getRandomPath( self ):
		path = []
		path = self.findRandomPath( self.root, path )
		return path

	def findRandomPath( self, node, path):
		path.append(node.value)
		if len( node.child ) > 0:
			randIndex = random.randint( 0, len(node.child)-1 )
			self.findRandomPath( node.child[ randIndex ], path)
		return path



	def printTree( self ):
		print "The root is " + str( self.root.value )
		for c in self.root.child:
			print str( self.root.value ) + " -> " + str( c.value )
		for c in self.root.child:
			self.printChilds( c )

	def printChilds( self, node ):
		for c in node.child:
			print str( node.value ) + " -> " + str( c.value )
		for c in node.child:
			if c != None:
				self.printChilds ( c )


class Node:
	def __init__( self, value ):
		self.value = value
		self.parent = None
		self.child = []

	def addChild ( self, value ):
		self.child.append( Node(value) )

