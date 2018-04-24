# cleanupDisk

## ini配置文件格式：
### 第一部分：root_file块，需要被修改权限的目录路径
* [root_file]

* key1=path1   //key为键值，path为路径

* key2=path2

### 第二部分：需要被删除的目录路径(包含多个块）
* [section_name]

* directory=value1  //需要被删除的路径

* days=value2       //预留天数，如何文件存在天数大于预留天数，则删除目录

* reserve=value3    //预留空间，单位为GB，如果目录下的文件总和大于预留空间，则删除目录


## 主要功能：
* 如果是root用户运行，读取配置ini文件，通过文件修改目录路径的权限位其他用户拥有所有权限。

* 如果是普通用户，读取配置文件，删除文件中需要删除的目录路径，但并非真正的删除，而是移动到备份目录下。
