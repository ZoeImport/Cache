#include <iostream>
#include <mariadb/conncpp.hpp>
#include <mariadb/conncpp/Connection.hpp>
#include <mariadb/conncpp/Driver.hpp>
#include <mariadb/conncpp/Exception.hpp>
#include <mariadb/conncpp/PreparedStatement.hpp>
#include <mariadb/conncpp/ResultSet.hpp>
#include <mariadb/conncpp/SQLString.hpp>
#include <mariadb/conncpp/Statement.hpp>
#include <mariadb/conncpp/jdbccompat.hpp>
#include <memory>
#include <ostream>
#include <string>


void insert_into(std::shared_ptr<sql::PreparedStatement> &stmnt,
                 sql::SQLString account, sql::SQLString password) {

  try {

    stmnt->setString(1, account);
    stmnt->setString(2, password);

    stmnt->executeUpdate();
    

  } catch (sql::SQLException &e) {
    std::cerr << "error to insert into " << e.what() << std::endl;
  }
}

void selectAll(std::shared_ptr<sql::Statement> &stmnt) {
  try {
    std::unique_ptr<sql::ResultSet> result{
        stmnt->executeQuery("select * from user_info")};
    while (result->next()) {
      std::cout << "| " << result->getString("account") << "\t| "
                << result->getString("password") <<" |  "<<result->getInt("id")<<" |"<<std::endl;
    }
  } catch (sql::SQLException &e) {
    std::cout << "error occured " << e.what() << std::endl;
  }
}

void select(std::shared_ptr<sql::Statement> &stmnt,sql::SQLString TableName,sql::SQLString column_1,sql::SQLString column_2) {
  try {
    
    sql::SQLString select_sql="select "+column_1+","+column_2+" "+"from "+TableName;
    std::unique_ptr<sql::ResultSet> result{stmnt->executeQuery(select_sql)};
    while (result->next()) {
      std::cout << "| " << result->getString(column_1) << "\t| "
                << result->getString(column_2) <<"\t|"<<std::endl;
    }
  } catch (sql::SQLException &e) {
    std::cerr<<"error occured "<<e.what()<<std::endl;
  }
}

void alter_table(std::shared_ptr<sql::Statement> &stmnt) {
  try {
  stmnt->executeUpdate("alter table user_info add id int primary key auto_increment");
  } catch (sql::SQLException&e) {
    std::cerr<<"error occured "<<e.what()<<std::endl;
  }
}



int main() {
  try {

    sql::Driver *driver = sql::mariadb::get_driver_instance();

    sql::SQLString url{"jdbc:mariadb://localhost:3306/Cpp"};
    sql::Properties properties{{"user", "zoe"}, {"password", "123456"}};

    std::unique_ptr<sql::Connection> conn(driver->connect(url, properties));

    if (!conn) {
      std::cerr << "connection error ..." << std::endl;
    }
    //insert into demo
    /*
    std::shared_ptr<sql::PreparedStatement> stmnt{conn->prepareStatement(
        "insert into user_info(account,password) value(?,?) ")};

    insert_into(stmnt, "Jack", "123321");
    */

    //select all demo
    
    // std::shared_ptr<sql::Statement> stmnt(conn->createStatement());
    // selectAll(stmnt);

    //select some column

    std::shared_ptr<sql::Statement> stmnt{
        conn->createStatement()};
    select(stmnt,"user_info","id","account");
    // alter table demo
    /*
    std::shared_ptr<sql::Statement> stmnt(conn->createStatement());
    alter_table(stmnt);
    */

    //
    
    // conn->close();
  } catch (sql::SQLException &e) {
    std::cerr << "error occured : " << e.what() << std::endl;
    return 1;
  }
  return 0;
}