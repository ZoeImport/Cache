use std::net::TcpListener;

fn main() {
    println!("hello");
    let listener = TcpListener::bind("127.0.0.1:10101").unwrap();
    for stream in listener.incoming() {
        let _stream = stream.unwrap();
        println!("connect establist");
    }
}
