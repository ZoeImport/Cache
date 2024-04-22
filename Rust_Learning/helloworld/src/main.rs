mod msg;
mod mytest;

use msg::msg::say::{max_one, MyInteger};

use crate::msg::msg::say;

fn main() {
    say::helloworld();
    say::echo(1);

    let myit1: MyInteger = MyInteger { val: 100 };
    let myit2: MyInteger = MyInteger { val: 200 };
    let res = max_one(&myit1, &myit2);
    println!("res:{:#?}", res.val())
}
