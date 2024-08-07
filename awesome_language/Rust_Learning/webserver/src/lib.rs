pub mod util {
    use std::{
        sync::{mpsc, Arc, Mutex},
        thread,
    };


    type Job = Box<dyn FnOnce() + Send + 'static>;
    enum Message {
        NewJob(Job),
        Terminate,
    }
    pub struct Worker {
        _id: usize,
        _thread: Option<thread::JoinHandle<()>>,
    }

    impl Worker {
        fn new(_id: usize, receiver: Arc<Mutex<mpsc::Receiver<Message>>>) -> Worker {
            let _thread = thread::spawn(move || loop {
                let message = receiver.lock().unwrap().recv().unwrap();
                match message {
                    Message::NewJob(job) => {
                        println!("worker {} got a job;excuting.", _id);
                        job();
                    }
                    Message::Terminate => {
                        println!("worker {} was told a terminate.", _id);
                        break;
                    }
                }
            });

            Worker {
                _id,
                _thread: Some(_thread),
            }
        }
    }
    pub struct ThreadPool {
        _workers: Vec<Worker>,
        sender: mpsc::Sender<Message>,
    }

    impl ThreadPool {
        pub fn new(size: usize) -> ThreadPool {
            assert!(size > 0);
            let (sender, receiver) = mpsc::channel();
            let receiver = Arc::new(Mutex::new(receiver));
            let mut _workers = Vec::with_capacity(size);
            for id in 0..size {
                _workers.push(Worker::new(id, Arc::clone(&receiver)));
            }
            ThreadPool { _workers, sender }
        }
        pub fn excute<F>(&self, f: F)
        where
            F: FnOnce() + Send + 'static,
        {
            let job = Box::new(f);
            self.sender.send(Message::NewJob(job)).unwrap();
        }
    }

    impl Drop for ThreadPool {
        fn drop(&mut self) {
            println!("Sending terminate message to all workers.");
            for _ in &mut self._workers {
                self.sender.send(Message::Terminate).unwrap();
            }
            println!("shuting down all workers.");
            for worker in &mut self._workers {
                println!("shuting down worker {}.", worker._id);
                if let Some(thread) = worker._thread.take() {
                    thread.join().unwrap();
                }
            }
        }
    }

}
