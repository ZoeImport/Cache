// #[allow(unused)]
pub mod say {
    use std::fmt::Display;

    pub trait CmpTrait {
        fn is_begger(a: &MyInteger, b: &MyInteger) -> bool;
    }
    pub struct MyInteger {
        pub(crate) val: u32,
    }
    impl MyInteger {
        pub fn val(&self) -> u32 {
            self.val
        }
    }

    impl CmpTrait for MyInteger {
        fn is_begger(a: &MyInteger, b: &MyInteger) -> bool {
            match a.val() > b.val() {
                true => true,
                false => false,
            }
        }
    }

    pub fn helloworld() {
        println!("hello world msg from firstmod")
    }

    pub fn echo<T>(info: T)
    where
        T: Display,
    {
        println!("this is {} ", info)
    }

    pub fn max_one<'c>(a: &'c MyInteger, b: &'c MyInteger) -> &'c MyInteger {
        if MyInteger::is_begger(a, b) {
            return a;
        }
        b
    }
}
