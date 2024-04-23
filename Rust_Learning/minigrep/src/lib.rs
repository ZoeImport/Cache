use std::{error::Error, fs};

pub struct Config {
    pub query: String,
    pub filename: String,
}

impl Config {
    pub fn new(args: &[String]) -> Result<Config, &str> {
        if args.len() < 3 {
            return Err("please enter correct args");
        }
        let query = args[1].clone();
        let filename = args[2].clone();
        Ok(Config { query, filename })
    }
}

pub fn search<'a>(query: &str, contexts: &'a str) -> Vec<&'a str> {
    let mut res = Vec::new();
    for line in contexts.lines() {
        if line.contains(query) {
            res.push(line);
        }
    }
    res
}

pub fn run(config: Config) -> Result<(), Box<dyn Error>> {
    let context = fs::read_to_string(config.filename)?;
    for line in context.lines() {
        if line.contains(&config.query) {
            println!("{line}");
        }
    }
    Ok(())
}
