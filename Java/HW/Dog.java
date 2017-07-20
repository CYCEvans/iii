package com.xxx.HW;

import java.io.*;

public class Dog implements Serializable,Animals{

	private static final long serialVersionUID = -4389793696694146488L;
	private String name;
	
	public Dog(String name) {
		this.name = name;
	}
	@Override
	public void speak() {
		System.out.println("This is Dog " + name + " speaking.");
	}
}
