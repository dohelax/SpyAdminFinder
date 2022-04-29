## SpyAdminFinder: Sitenin yönetici panelini bulmanın kolay yolu.

*SpyAdminFinder bir web sitesinin yönetici panelini bulmak isteyen yöneticiler/pentesterler için **Python 3.x**'te yeniden yazılmış bir Apache2 Lisanslı yardımcı programdır. Başka birçok araç var ama onlar kadar etkili ve güvenli değil. Evet, SpyAdminFinder tor kullanma ve kimliğinizi gizleme yeteneğine sahiptir*

* ## Requirements
    ![PyPI](https://img.shields.io/pypi/v/argparse.svg?label=argparse)
    ![PyPI](https://img.shields.io/pypi/v/colorama.svg?label=colorama)
    ![PyPI](https://img.shields.io/pypi/v/PySocks.svg?label=PySocks)
    ![PyPI](https://img.shields.io/pypi/v/tqdm.svg?label=tqdm)
    ![PyPI](https://img.shields.io/pypi/v/requests.svg?label=requests)
    * #### Linux
       ```
       sudo apt install tor
       sudo apt install python3-socks  (optional)
       pip3 install --user -r requirements.txt
       ```

    * #### Windows
       download [tor expert bundle](https://dist.torproject.org/torbrowser/8.0.8/tor-win32-0.3.5.8.zip)
       `pip3 install -r requirements.txt`

* ## Usage
   
    * #### Linux
       ```
       git clone https://github.com/mIcHyAmRaNe/okadminfinder3.git
       cd okadminfinder3
       chmod +x okadminfinder.py
       python3 okadminfinder.py
       ```

    * #### Windows
       download & extract [zip](https://github.com/mIcHyAmRaNe/okadminfinder3/archive/master.zip)
       ```
       cd okadminfinder3
       py -3 okadminfinder.py
       ```

    * #### [Pentestbox](https://pentestbox.com) (same procedure as Linux)
        you can add an alias by adding this line: `okadminfinder=py -3 "%pentestbox_ROOT%/bin/Path/to/okadminfinder3/okadminfinder.py" $*` to `C://Pentestbox/bin/customtools/customaliases` file and so you'll be able to launch it using      `okadminfinder`
