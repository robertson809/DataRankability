/**
 * Name: CycleFinder.java
 * Purpose: The goal of this program is to locate and tabulate any cycles 
 * 			in a directed graph. A user should input an adjacency matrix
 * 			in order to receive a histogram of the number and types of cycles.
 * Authors: Dr. Thomas Cameron, Joseph Campbell
 * Starting Date: May 17th, 2019
 * Last Date Edited: May 25th, 2019
 * Current Version: 1.4.2
 */
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.StringTokenizer;
import java.util.TreeSet;

public class CycleFinder {

	public static void output(int[][] arr)
	{
		for (int[] x : arr) 
		{
			System.out.println(Arrays.toString(x));
		}
	}
	
	public static void main(String[] args) throws IOException {
		/** INPUT **/
		BufferedReader br = new BufferedReader(new FileReader("./Big_East/matrices/binaryMatrix1998.txt"));
		PrintWriter pw1 = new PrintWriter(new BufferedWriter(new FileWriter("results/outCycles.txt")));
		PrintWriter pw2 = new PrintWriter(new BufferedWriter(new FileWriter("results/histogram.txt")));
		StringTokenizer st = new StringTokenizer(br.readLine());
		
		/** TESTING **/
		TreeSet<CycleList> se = new TreeSet<CycleList>();
		
		CycleList<Integer> a = new CycleList<Integer>();
		a.add(1);
		a.add(2);
		a.add(4);
		
		CycleList<Integer> b = new CycleList<Integer>();
		b.add(4);
		b.add(2);
		b.add(1);
		
		//System.out.println(a.equals(b));
		
		se.add(b);
		se.add(a);
		
		//System.out.println(se.size());
		//System.out.println(se);
		
		/** TESTING **/
		
		ArrayList<Integer> firstRow = new ArrayList<Integer>();
		while (st.hasMoreTokens())
		{
			firstRow.add(Integer.parseInt(st.nextToken()));
		}
		int n = firstRow.size();
		int[][] adjMat = new int[n][n];
		int[][] adjMatTransverse = new int[n][n];
		for (int i = 1; i < n; i++)
		{
			st = new StringTokenizer(br.readLine());
			for (int j = 0; j < n; j++)
			{
				adjMat[i][j] = Integer.parseInt(st.nextToken());
				adjMatTransverse[j][i] = adjMat[i][j];
			}
		}
		for (int i = 0; i < n; i++)
		{
			adjMat[0][i] = firstRow.get(i);
			adjMatTransverse[i][0] = adjMat[0][i];
		}

		//output(adjMat);
		//output(adjMatTransverse);
		
		HashSet<Integer> rootsVisited = new HashSet<Integer>();
		int[] x = new int[n];
		for (int i = 0; i < n; i++) {x[i] = i;}
		
		int toDo = 0;
		TreeSet<CycleList<Integer>> allCycles = new TreeSet<CycleList<Integer>>();
 		while (rootsVisited.size() < n)
		{
			CycleTree tree = new CycleTree(adjMatTransverse, new Node(toDo));
			rootsVisited.addAll(tree.buildTree());
			//System.out.println(tree.cyclesFound);
			allCycles.addAll(tree.cyclesFound);
			L: for (int k : x)
			{
				if (!rootsVisited.contains(k))
				{
					toDo = k;
					break L;
				}
			}
		}
 		//System.out.println(allCycles);
 		HashMap<Integer, Integer> map = new HashMap<Integer, Integer>();
 		for (CycleList<Integer> t : allCycles)
 		{
 			if (map.containsKey(t.size()))
 			{
 				map.put((Integer) t.size(), map.get(t.size()) + 1);
 			}
 			else
 			{
 				map.put((Integer) t.size(), 1);
 			}
 		}
		
 		for (int k : map.keySet())
 		{
 			//System.out.println("There are " + map.get(k) + " distinct " + k + "-cycles in this graph");
 			pw2.println("(" + k + "," + map.get(k) + ")");
 		}
 		pw2.close();
 		
 		for (CycleList z : allCycles)
 		{
 			pw1.println(z.toString());
 		}
 		pw1.close();
	}

}

class CycleTree
{
	public int[][] mat;
	public Node rootNode;
	public HashSet<Integer> rootsSeen = new HashSet<Integer>();
	public TreeSet<CycleList<Integer>> cyclesFound = new TreeSet<CycleList<Integer>>();
	
	public CycleTree(int[][] m, Node root)
	{
		mat = m;
		rootNode = root;
		rootsSeen.add(rootNode.value);
	}
	
	public HashSet<Integer> buildTree()
	{
		LinkedList<Node> queue = new LinkedList<Node>();
		queue.add(rootNode);
		while (queue.size() > 0)
		{
			Node n = queue.poll();
			//System.out.println(n);
			for (int i = 0; i < mat.length; i++)
			{
				if (mat[n.value][i] == 1)
				{
					ArrayList tempAnc = (ArrayList) (n.ancestors).clone();
					tempAnc.add(n);
					ArrayList tempAncVal = (ArrayList) (n.ancestorVals).clone();
					tempAncVal.add(n.value);
					
					Node x = new Node(i, tempAnc, tempAncVal);
					rootsSeen.add(x.value);
					if (x.isCyclic() == -1)
					{
						queue.add(x);
						//System.out.println("Added " + x + " to the queue.");
					}
					else // cycle located
					{
						ArrayList<Integer> cycle = x.cycle();
						//System.out.println(cycle);
						CycleList<Integer> temp = new CycleList<Integer>();
						temp.list = (ArrayList<Integer>) cycle.clone();
						cyclesFound.add(temp);
						//System.out.println("There is a " + x.isCyclic() + "-cycle in this graph: " + x.ancestorVals + ", " + x.value);
					}
				}
			}
		}
		return rootsSeen;
	}

}

class Node
{
	public int value;
	public ArrayList<Node> ancestors;
	public ArrayList<Integer> ancestorVals;
	
	public Node(int val)
	{
		value = val;
		ancestors = new ArrayList<Node>();
		ancestorVals = new ArrayList<Integer>();
	}
	
	public Node(int val, ArrayList<Node> anc, ArrayList<Integer> ancVal)
	{
		value = val;
		ancestors = anc; 
		ancestorVals = ancVal;
	}
	
	public int isCyclic()
	{
		if (ancestorVals.contains(value))
		{
			return ancestors.size() - ancestorVals.indexOf(value);
		}
		return -1;
	}
	
	public ArrayList<Integer> cycle()
	{
		if (this.isCyclic() >= 0)
		{
			ArrayList<Integer> ans = new ArrayList<Integer>(ancestorVals.subList(ancestorVals.indexOf(value), ancestorVals.size()));
			//System.out.println("There is a " + this.isCyclic() + "-cycle in this graph: "+ ans);
			return ans;
		}
		return null;
	}
	
	public String toString()
	{
		return "(" +  value + ", " + ancestorVals + ")";
	}
}

class CycleList<Type> implements Comparable<CycleList>
{
	public ArrayList<Type> list = new ArrayList<Type>();
	
	public CycleList()
	{
		
	}
	
	public int size() {
		// TODO Auto-generated method stub
		return list.size();
	}

	public CycleList(ArrayList<? extends Type> a)
	{
		list.addAll(a);
	}
	
	public void add(Type a)
	{
		list.add(a);
	}
	
	public String toString()
	{
		return list.toString();
	}
	
	@Override
	public boolean equals(Object obj) {
		if (this == obj) {
			return true;
		}
		if (obj == null) {
			return false;
		}
		if (getClass() != obj.getClass()) {
			return false;
		}
		CycleList other = (CycleList) obj;
		ArrayList<Type> dual = new ArrayList<Type>();
		dual.addAll(list);
		dual.addAll(list);
		if (list == null) {
			if (other.list != null) {
				return false;
			}
		} else if (Collections.indexOfSubList(dual, other.list) == -1) {
			return false;
		}
		return true;
	}



	@Override
	public int compareTo(CycleList o) {
		if (this.equals(o)) {return 0;}
		else
		{
			if (this.list.size() > o.list.size()) {return 1;}
			else {return -1;}
		}
	}
	
	
}

/**
Examples:
0 1 0 0 1
1 0 1 1 0
1 0 0 0 0
1 0 0 0 1
0 0 1 0 0

0 0 1 1 1 0 0 1
1 0 1 1 1 1 0 1
0 0 0 1 0 1 0 0
0 0 0 0 1 0 0 0
0 0 1 0 0 1 0 1
1 0 0 1 0 0 0 0
1 1 1 1 1 1 0 1
0 0 1 1 0 1 0 0

0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 1 0 0 0 0 0 0 0 0 1 0
0 1 0 0 1 0 0 0 0 0 0 0 0 1 0 0
0 1 1 1 0 0 1 1 0 0 0 0 0 1 0 0
0 0 0 0 0 0 1 0 0 0 0 0 1 0 0 1
0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 1
0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 1 0 0 1
0 0 0 0 0 0 0 0 1 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0
0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
**/