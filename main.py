# conda activate webservicep2plending //untuk mengaktifkan environtment
# uvicorn webservice.main:app --reload //untuk mereload agar setiap membuat webserver akan otomatis reload code terbaru (tidak perlu dimatikan lalu dinyalakan)


from typing import Union #untuk menunjukkan bahwa suatu variabel bisa memiliki lebih dari satu tipe data.
from fastapi import FastAPI,Response,Request,HTTPException #mengimpor kelas FastAPI dan beberapa kelas lain yang dibutuhkan dari modul fastapi
from fastapi.middleware.cors import CORSMiddleware #mengimpor middleware yang digunakan untuk menangani kebijakan CORS (Cross-Origin Resource Sharing) pada aplikasi FastAPI.
import sqlite3 #mengimpor modul sqlite3 untuk melakukan operasi database dengan SQLite.

app = FastAPI() #Membuat instance FastAPI yang akan digunakan untuk mengkonfigurasi API.

app.add_middleware( #Memulai penambahan middleware ke aplikasi FastAPI.
	CORSMiddleware, #Menggunakan middleware CORSMiddleware yang telah diimpor sebelumnya untuk menangani kebijakan CORS.
	allow_origins=["*"], #Mengatur daftar domain yang diizinkan untuk mengakses API. Dalam kasus ini, menggunakan tanda bintang (*) untuk mengizinkan akses dari semua domain.
	allow_credentials=True, #Mengatur apakah permintaan dengan kredensial (seperti cookies, auth headers) diizinkan. Pada kasus ini, diatur ke True untuk mengizinkan penggunaan kredensial.
	allow_methods=["*"], #Mengatur daftar metode HTTP yang diizinkan untuk digunakan dalam akses CORS. Dengan menggunakan tanda bintang (*), semua metode HTTP diizinkan (GET, POST, PUT, dll.).
	allow_headers=["*"], #Mengatur daftar header HTTP yang diizinkan dalam akses CORS. Dengan menggunakan tanda bintang (*), semua header diizinkan.
)


@app.get("/") #Mendefinisikan endpoint untuk URI root ("/"). Fungsi read_root akan dijalankan ketika ada permintaan GET ke URI root, dan akan mengembalikan objek JSON {"Hello": "World"}.
def read_root(): 
    return {"Hello": "World"} 

@app.get("/mahasiswa/{nim}") #Mendefinisikan endpoint untuk URI "/mahasiswa/{nim}". {nim} adalah bagian dari URI yang dapat digantikan dengan nilai nim (Nomor Induk Mahasiswa) yang diberikan dalam permintaan. Fungsi ambil_mhs akan dijalankan ketika ada permintaan GET ke URI tersebut, dan akan mengembalikan objek JSON dengan nama mahasiswa yang sesuai dengan nim yang diberikan.
def ambil_mhs(nim:str): 
    return {"nama": "Fachturozi"} 

@app.get("/mahasiswa2/") #Mendefinisikan endpoint untuk URI "/mahasiswa2/". Fungsi ambil_mhs2 tidak memiliki parameter, sehingga akan mengembalikan objek JSON dengan nama mahasiswa tertentu.
def ambil_mhs2(nim:str): 
    return {"nama": "Fachturozi 2"} 

@app.get("/daftar_mhs/") #Mendefinisikan endpoint untuk URI "/daftar_mhs/". Fungsi daftar_mhs memiliki dua parameter query string, yaitu id_prov dan angkatan. Fungsi ini akan mengembalikan objek JSON yang berisi pesan dengan nilai id_prov dan angkatan, serta daftar data mahasiswa dalam bentuk JSON array.
def daftar_mhs(id_prov:str,angkatan:str): 
    return {"query":" idprov: {}  ; angkatan: {} ".format(id_prov,angkatan),"data":[{"nim":"1234"},{"nim":"1235"}]} 

# panggil sekali saja
@app.get("/init/") #Mendefinisikan endpoint untuk URI "/init/". Ini adalah endpoint yang digunakan untuk inisialisasi database.
def init_db(): #Mendefinisikan fungsi init_db yang akan dijalankan ketika ada permintaan GET ke URI "/init/". Fungsi ini bertanggung jawab untuk membuat tabel mahasiswa di database SQLite.
  try: #Memulai blok try untuk mengeksekusi potongan kode yang mungkin menimbulkan exception.
    DB_NAME = "upi.db" #Mendefinisikan nama database sebagai "upi.db".
    con = sqlite3.connect(DB_NAME) #Membuka koneksi ke database SQLite dengan nama "upi.db" dan menyimpan koneksi dalam variabel con.
    cur = con.cursor() #Membuat objek cursor untuk berinteraksi dengan database.
    create_table = """ CREATE TABLE mahasiswa( 
            ID      	INTEGER PRIMARY KEY 	AUTOINCREMENT,
            nim     	TEXT            	NOT NULL,
            nama    	TEXT            	NOT NULL,
            id_prov 	TEXT            	NOT NULL,
            angkatan	TEXT            	NOT NULL,
            tinggi_badan  INTEGER
        )  
        """ # Mendefinisikan string create_table yang berisi perintah SQL untuk membuat tabel mahasiswa.
    cur.execute(create_table) #Mengeksekusi perintah SQL untuk membuat tabel mahasiswa.

    con.commit #Melakukan commit perubahan ke database.
  except: #Menangkap dan menangani exception yang terjadi selama eksekusi kode di dalam blok try.
           return ({"status":"terjadi error"}) #Mengembalikan pesan JSON "status: terjadi error" jika terjadi exception selama eksekusi.
  finally: #Blok finally digunakan untuk menjalankan kode yang harus dijalankan terlepas dari apakah terjadi exception atau tidak.
           con.close() #Menutup koneksi ke database setelah selesai melakukan inisialisasi tabel.
    
  return ({"status":"ok, db dan tabel berhasil dicreate"}) #

from pydantic import BaseModel #Mengimpor kelas BaseModel dari modul pydantic. Kelas ini digunakan sebagai dasar untuk mendefinisikan model Pydantic.

from typing import Optional #Mengimpor tipe Optional dari modul typing. Tipe Optional digunakan untuk menunjukkan bahwa sebuah atribut bisa jadi memiliki nilai None.

class Mhs(BaseModel): #Mendefinisikan kelas Mhs yang merupakan subkelas dari BaseModel. Ini adalah model Pydantic untuk data mahasiswa.
   nim: str #Mendefinisikan atribut nim dengan tipe data str. Atribut ini merepresentasikan NIM mahasiswa.
   nama: str #Mendefinisikan atribut nama dengan tipe data str. Atribut ini merepresentasikan nama mahasiswa.
   id_prov: str #Mendefinisikan atribut id_prov dengan tipe data str. Atribut ini merepresentasikan ID provinsi asal mahasiswa.
   angkatan: str #Mendefinisikan atribut angkatan dengan tipe data str. Atribut ini merepresentasikan tahun angkatan mahasiswa.
   tinggi_badan: Optional[int] | None = None  # yang boleh null hanya ini


#status code 201 standard return creation
#return objek yang baru dicreate (response_model tipenya Mhs)
@app.post("/tambah_mhs/", response_model=Mhs,status_code=201) #Mendefinisikan endpoint POST dengan path /tambah_mhs/. response_model=Mhs menunjukkan bahwa response dari endpoint ini akan berupa objek sesuai dengan model Mhs. status_code=201 menandakan bahwa jika penambahan data berhasil, response code yang dikembalikan adalah 201 (Created).
def tambah_mhs(m: Mhs,response: Response, request: Request): #Mendefinisikan fungsi tambah_mhs yang akan dijalankan ketika endpoint /tambah_mhs/ diakses. Fungsi ini menerima tiga parameter: m (objek Mhs yang akan ditambahkan), response (objek response untuk dikonfigurasi), dan request (objek request untuk mendapatkan informasi tentang request yang masuk).
   try: #Memulai blok percobaan untuk mengeksekusi kode. Jika terjadi exception, akan melompat ke blok except.
       DB_NAME = "upi.db" #Mendefinisikan nama database yang akan digunakan (upi.db).
       con = sqlite3.connect(DB_NAME) #Membuka koneksi ke database SQLite dengan nama upi.db.
       cur = con.cursor() #Membuat objek cursor untuk mengeksekusi perintah SQL.
       # hanya untuk test, rawal sql injecttion, gunakan spt SQLAlchemy
       cur.execute("""insert into mahasiswa (nim,nama,id_prov,angkatan,tinggi_badan) values ( "{}","{}","{}","{}",{})""".format(m.nim,m.nama,m.id_prov,m.angkatan,m.tinggi_badan)) #Mengeksekusi perintah SQL untuk memasukkan data mahasiswa ke dalam tabel mahasiswa dalam database.
       con.commit() #Melakukan commit untuk menyimpan perubahan ke dalam database.
   except: #Blok yang akan dieksekusi jika terjadi exception selama eksekusi kode di dalam blok try.
       print("oioi error") #Mencetak tulisan
       return ({"status":"terjadi error"}) #Mengembalikan response JSON yang menyatakan terjadi error jika ada exception.  
   finally: #Blok yang akan dieksekusi setelah blok try selesai, terlepas dari apakah terjadi exception atau tidak.
       con.close() #Menutup koneksi ke database setelah selesai digunakan.
   response.headers["Location"] = "/mahasiswa/{}".format(m.nim) #Mengatur header Location pada response untuk menunjukkan URL lokasi data mahasiswa yang baru ditambahkan.
   print(m.nim) #Mencetak informasi nim
   print(m.nama) #Mencetak informasi nama
   print(m.angkatan) #Mencetak informasi angkatan
  
   return m #Mengembalikan data mahasiswa yang baru ditambahkan sebagai response.



@app.get("/tampilkan_semua_mhs/") #Mendefinisikan endpoint GET dengan path /tampilkan_semua_mhs/. Endpoint ini digunakan untuk menampilkan semua data mahasiswa.
def tampil_semua_mhs(): #Mendefinisikan fungsi tampil_semua_mhs yang akan dijalankan ketika endpoint /tampilkan_semua_mhs/ diakses. Fungsi ini tidak menerima parameter.
   try: #Memulai blok percobaan untuk mengeksekusi kode. Jika terjadi exception, akan melompat ke blok except.
       DB_NAME = "upi.db" #Mendefinisikan nama database yang akan digunakan (upi.db).
       con = sqlite3.connect(DB_NAME) #Membuka koneksi ke database SQLite dengan nama upi.db.
       cur = con.cursor() #Membuat objek cursor untuk mengeksekusi perintah SQL.
       recs = [] #Membuat list recs untuk menyimpan hasil query.
       for row in cur.execute("select * from mahasiswa"): #Melakukan iterasi melalui setiap baris data mahasiswa yang diperoleh dari eksekusi query SQL select * from mahasiswa.
           recs.append(row) #Menambahkan setiap baris data ke dalam list recs.
   except: #Blok yang akan dieksekusi jika terjadi exception selama eksekusi kode di dalam blok try.
       return ({"status":"terjadi error"}) #Mengembalikan response JSON yang menyatakan terjadi error jika ada exception.
   finally: #Blok yang akan dieksekusi setelah blok try selesai, terlepas dari apakah terjadi exception atau tidak.
       con.close() #Menutup koneksi ke database setelah selesai digunakan.
   return {"data":recs} #Mengembalikan response JSON yang berisi data mahasiswa yang telah diambil dari database dalam bentuk list recs.

from fastapi.encoders import jsonable_encoder #Mengimpor fungsi jsonable_encoder dari modul fastapi.encoders. Fungsi ini digunakan untuk mengonversi objek Pydantic model ke JSON serializable.


@app.put("/update_mhs_put/{nim}",response_model=Mhs) #Mendefinisikan endpoint PUT dengan path /update_mhs_put/{nim}. Endpoint ini digunakan untuk mengupdate data mahasiswa berdasarkan NIM, dengan response berupa objek Mhs.
def update_mhs_put(response: Response,nim: str, m: Mhs ): #Mendefinisikan fungsi update_mhs_put yang akan dijalankan ketika endpoint /update_mhs_put/{nim} diakses. Fungsi ini menerima parameter response (objek Response dari FastAPI), nim (NIM mahasiswa yang akan diupdate), dan m (data mahasiswa baru yang akan diupdate).
    #update keseluruhan
    #karena key, nim tidak diupdape
    try: #Memulai blok percobaan untuk mengeksekusi kode. Jika terjadi exception, akan melompat ke blok except.
       DB_NAME = "upi.db" #Mendefinisikan nama database yang akan digunakan (upi.db).
       con = sqlite3.connect(DB_NAME) #Membuka koneksi ke database SQLite dengan nama upi.db.
       cur = con.cursor() #Membuat objek cursor untuk mengeksekusi perintah SQL.
       cur.execute("select * from mahasiswa where nim = ?", (nim,) )  #Melakukan query SQL untuk mendapatkan data mahasiswa dengan NIM tertentu.
       existing_item = cur.fetchone() #Mengambil hasil query pertama sebagai data mahasiswa yang akan diupdate.
    except Exception as e: #Blok yang akan dieksekusi jika terjadi exception selama eksekusi kode di dalam blok try. Exception akan ditangkap dan pesan error akan dikirimkan sebagai detail dari HTTP response.
        raise HTTPException(status_code=500, detail="Terjadi exception: {}".format(str(e))) #Untuk menghentikan eksekusi fungsi dan mengembalikan sebuah HTTPException dengan status code 500 (Internal Server Error) serta detail pesan yang menjelaskan bahwa terjadi exception dalam bentuk string dari variabel e.
    
    if existing_item:  #data ada 
            print(m.tinggi_badan) #Mencetak data tinggi badan
            cur.execute("update mahasiswa set nama = ?, id_prov = ?, angkatan=?, tinggi_badan=? where nim=?", (m.nama,m.id_prov,m.angkatan,m.tinggi_badan,nim)) #Melakukan query SQL untuk melakukan update data mahasiswa dengan NIM tertentu.
            con.commit() #Melakukan commit terhadap perubahan data ke dalam database.
            response.headers["location"] = "/mahasiswa/{}".format(m.nim) #Mengatur header location pada response untuk menunjukkan URL lokasi data mahasiswa yang telah diupdate.
    else:  # data tidak ada
            print("item not found") #Mencetak tulisan
            raise HTTPException(status_code=404, detail="Item Not Found") #Untuk menimbulkan pengecualian HTTPException dengan kode status 404 (Not Found) dan detail pesan yang menyatakan "Item Not Found".
      
    con.close() #Menutup koneksi ke database setelah selesai digunakan.
    return m #Mengembalikan data mahasiswa yang telah diupdate sebagai response dari endpoint.


# khusus untuk patch, jadi boleh tidak ada
# menggunakan "kosong" dan -9999 supaya bisa membedakan apakah tdk diupdate ("kosong") atau mau
# diupdate dengan dengan None atau 0
class MhsPatch(BaseModel): #Mendefinisikan kelas MhsPatch yang merupakan turunan dari BaseModel dari Pydantic. Ini berarti MhsPatch akan memiliki semua fitur yang disediakan oleh BaseModel, termasuk validasi data.
   nama: str | None = "kosong" #Mendefinisikan atribut nama dengan tipe data str yang dapat bernilai None jika tidak ada nilai yang diberikan. Jika tidak ada nilai yang diberikan, maka nilai defaultnya adalah "kosong".
   id_prov: str | None = "kosong" #Mendefinisikan atribut id_prov dengan tipe data str yang juga dapat bernilai None jika tidak ada nilai yang diberikan. Jika tidak ada nilai yang diberikan, maka nilai defaultnya adalah "kosong".
   angkatan: str | None = "kosong" #Mendefinisikan atribut angkatan dengan tipe data str yang juga dapat bernilai None jika tidak ada nilai yang diberikan. Jika tidak ada nilai yang diberikan, maka nilai defaultnya adalah "kosong".
   tinggi_badan: Optional[int] | None = -9999  #yang boleh null hanya ini



@app.patch("/update_mhs_patch/{nim}",response_model = MhsPatch) #Mendefinisikan decorator untuk endpoint update_mhs_patch dengan metode PATCH. Metode PATCH digunakan untuk mengirimkan data parsial yang akan diperbarui ke server. Parameter response_model digunakan untuk menentukan model data yang akan dikembalikan oleh endpoint setelah berhasil melakukan update. Dalam hal ini, model yang digunakan adalah MhsPatch.
def update_mhs_patch(response: Response, nim: str, m: MhsPatch ): #Mendefinisikan fungsi update_mhs_patch yang akan dieksekusi ketika endpoint diakses. 
    try: #Blok try digunakan untuk menangani eksekusi kode yang mungkin menimbulkan exception.
      print(str(m)) #Mencetak objek m (yang merupakan instans dari MhsPatch) ke dalam bentuk string. Ini digunakan untuk debugging dan memastikan bahwa data yang dikirim sesuai.
      DB_NAME = "upi.db" #Mendefinisikan nama file database SQLite yang akan digunakan.
      con = sqlite3.connect(DB_NAME) #Membuka koneksi ke database SQLite.
      cur = con.cursor() #Membuat objek cursor untuk berinteraksi dengan database.
      cur.execute("select * from mahasiswa where nim = ?", (nim,) )  #tambah koma untuk menandakan tupple
      existing_item = cur.fetchone() #Mengambil satu baris data hasil query sebagai objek existing_item.
    except Exception as e: #Blok except digunakan untuk menangkap exception yang mungkin terjadi selama eksekusi kode di dalam blok try. Jika terjadi exception, akan dianggap bahwa terjadi kesalahan saat mengakses database, dan akan diangkat HTTPException dengan kode status 500 (Internal Server Error) beserta detail kesalahan yang terjadi.
      raise HTTPException(status_code=500, detail="Terjadi exception: {}".format(str(e))) # misal database down  
    
    if existing_item:  #data ada, lakukan update
        sqlstr = "update mahasiswa set " #asumsi minimal ada satu field update
        # todo: bisa direfaktor dan dirapikan
        if m.nama!="kosong": #Jika data nama kosong
            if m.nama!=None: #Jika data nama kosong
                sqlstr = sqlstr + " nama = '{}' ,".format(m.nama) #Mengupdate variabel sqlstr dengan string SQL untuk memperbarui data nama dengan nilai yang ada pada objek m.
            else: #Jika tidak kosong
                sqlstr = sqlstr + " nama = null ," #Maka tidak diupdate
        
        if m.angkatan!="kosong": #Jika data angkatan kosong
            if m.angkatan!=None: #Jika data angkatan kosong
                sqlstr = sqlstr + " angkatan = '{}' ,".format(m.angkatan) #Mengupdate variabel sqlstr dengan string SQL untuk memperbarui data angkatan dengan nilai yang ada pada objek m.
            else: #Jika tidak kosong
                sqlstr = sqlstr + " angkatan = null ," #Maka tidak diupdate
        
        if m.id_prov!="kosong": #Jika data provinsi kosong
            if m.id_prov!=None: #Jika data provinsi kosong
                sqlstr = sqlstr + " id_prov = '{}' ,".format(m.id_prov) #Mengupdate variabel sqlstr dengan string SQL untuk memperbarui data provinsi dengan nilai yang ada pada objek m.
            else: #Jika tidak Kosong
                sqlstr = sqlstr + " id_prov = null, " #Maka tidak diupdate

        if m.tinggi_badan!=-9999: #Jika data tinggi badan -9999
            if m.tinggi_badan!=None: #Jika data tinggi badan kosong
                sqlstr = sqlstr + " tinggi_badan = {} ,".format(m.tinggi_badan) #Mengupdate variabel sqlstr dengan string SQL untuk memperbarui data tinggi badan dengan nilai yang ada pada objek m.
            else: #Jika tidak kosong
                sqlstr = sqlstr + " tinggi_badan = null ," #Maka tidak diupdate

        sqlstr = sqlstr[:-1] + " where nim='{}' ".format(nim)  #buang koma yang trakhir  
        print(sqlstr) #Mencetak sqlstr
        try: #Blok try digunakan untuk menangani eksekusi kode yang mungkin menimbulkan exception.
            cur.execute(sqlstr) #Mengeksekusi query SQL untuk melakukan partial update data mahasiswa.
            con.commit() #Melakukan commit terhadap perubahan data ke dalam database.
            response.headers["location"] = "/mahasixswa/{}".format(nim) #Mengatur header Location pada respons HTTP untuk menunjukkan lokasi data mahasiswa yang telah diperbarui.
        except Exception as e: #Blok except digunakan untuk menangkap exception yang mungkin terjadi selama eksekusi kode di dalam blok try. Jika terjadi exception, akan dianggap bahwa terjadi kesalahan saat mengakses database, dan akan diangkat HTTPException dengan kode status 500 (Internal Server Error) beserta detail kesalahan yang terjadi.
            raise HTTPException(status_code=500, detail="Terjadi exception: {}".format(str(e))) #misal database down
        

    else:  # data tidak ada 404, item not found
         raise HTTPException(status_code=404, detail="Item Not Found") #misal data tidak ditemukan
   
    con.close() #Menutup koneksi ke database setelah selesai melakukan update.
    return m #Mengembalikan objek m yang berisi data mahasiswa yang telah diperbarui.
  
    
@app.delete("/delete_mhs/{nim}") #Mendefinisikan route untuk HTTP method DELETE pada path /delete_mhs/{nim}, di mana {nim} adalah parameter NIM mahasiswa yang akan dihapus.
def delete_mhs(nim: str): #Mendefinisikan fungsi delete_mhs yang memiliki parameter nim sebagai NIM mahasiswa yang akan dihapus.
    try: #Membuka blok percobaan untuk mengeksekusi operasi penghapusan data.
       DB_NAME = "upi.db" #Mendefinisikan nama database yang akan digunakan.
       con = sqlite3.connect(DB_NAME) #Membuat koneksi ke database SQLite dengan menggunakan nama database yang sudah didefinisikan.
       cur = con.cursor() #Membuat objek cursor untuk mengeksekusi perintah SQL.
       sqlstr = "delete from mahasiswa  where nim='{}'".format(nim) #Mendefinisikan string SQL untuk menghapus data mahasiswa dengan NIM yang sesuai dengan nilai parameter nim.      
       print(sqlstr) # debug 
       cur.execute(sqlstr) #Mengeksekusi perintah SQL untuk menghapus data mahasiswa.
       con.commit() #Melakukan commit untuk menyimpan perubahan ke database.
    except: #Menangani exception yang terjadi selama proses penghapusan data.
       return ({"status":"terjadi error"}) #Mengembalikan pesan kesalahan jika terjadi error selama proses penghapusan data.
    finally: #Blok yang selalu dieksekusi, baik terjadi error maupun tidak.
       con.close() #Menutup koneksi ke database setelah selesai melakukan operasi penghapusan.
    
    return {"status":"ok"} #Mengembalikan pesan status berhasil jika data berhasil dihapus.
