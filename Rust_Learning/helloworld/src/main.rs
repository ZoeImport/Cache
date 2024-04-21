fn main() {
    println!("Hello, world!");
    let  str=String::from(" can you speak Chinese ? ");
    first_world(str);
}   

fn first_world(str:&String)->usize{
    str.len()
}

