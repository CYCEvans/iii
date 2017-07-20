package com.xxx.HW;
import java.util.*;
class BigInteger{
	private String string; 
	public BigInteger(String string) {
		this.string= string;
	}
	@Override
	public String toString() {
		return "string=" + string ;
	}
}

public class HW08_1 {

	public static void main(String[] args) {
		ArrayList arrL = new ArrayList();
		arrL.add(new Integer(100));
		arrL.add(new Double(3.14));
		arrL.add(new Long(21L));
		arrL.add(new Short("100"));
		arrL.add(new Double(5.1));
		arrL.add("Kitty");
		arrL.add(new Integer(100));
		arrL.add(new Object());
		arrL.add("Snoopy");
		arrL.add(new BigInteger("1000"));
		Iterator st = arrL.iterator();
		while (st.hasNext()){
			System.out.println(st.next());
		}
		for(Iterator st2= arrL.iterator();st2.hasNext();){
			System.out.println(st2.next());
		}
		for(Object obj:arrL){
			System.out.println(obj);
		}
		for(Iterator st3= arrL.iterator();st3.hasNext();){
			if(!(st3.next() instanceof Number)){
				st3.remove();
			}
		}
		for(Object obj:arrL){
			System.out.println(obj);
		}
	}
}
