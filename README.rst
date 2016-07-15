Open Project Migration
======================

개요
----

`네이버 오픈 프로젝트`_\ 를 GitHub로 migration 하는 CLI(Comamnd Line
Interface) 프로그램입니다. 아래와 같은 기능을 갖추고 있습니다.

기능
----

#. 게시판, 이슈의 첨부파일들을 포함한 글과 댓글들을 GitHub 이슈로
   마이그레이션.
#. 다운로드의 게시물과 파일들을 GitHub 릴리즈로 마이그레이션.
#. Git/SVN 소스코드 저장소 마이그레이션.

Dependencies
------------

-  Python 2.7 이상
-  Git 2.7 이상

사용법
------

-  유효한 GitHub, NAVER 계정을 준비해주세요.
-  Python과 Git을 설치해주세요.
-  이 프로젝트를 다운로드 받아주세요.
-  터미널에서 pip를 이용해 프로그램에 필요한 python 패키지를
   설치해주세요.

    $ pip install –editable .

-  프로그램을 실행시켜주세요

    $ migration

-  이제 프로그램의 지시에 따라 각종 정보를 입력해주시면 자동으로
   migration이 진행됩니다.

-  도움말을 참고하셔서 직접 터미널에 옵션을 입력하는 것도
   가능합니다 (migration --help 명령어로 확인 가능)


-  미리 Github 저장소를 만들어주시고 아래 안내를 통해 위키까지
   만들어주시면 더욱 편한 사용이 가능합니다.

주의사항
--------

-  **프로그램 실행 후 반드시 아래 주소로 들어가셔서 위키의 첫 페이지를
   만들어주세요!! https://github.com/{계졍명}/{저장소명}/wiki**

   |위키 만들기|

-  **자신의 오픈 프로젝트가 사용하고 있는 버전 컨트롤 시스템의 종류를
   정확히 입력해주세요. (git or svn) 정확하지 않으면 소스코드 저장소
   migration이 진행되지 않습니다.**
-  **정확한 계정명을 입력하시지 않으면 프로그램이 동작하지 않습니다**

.. _네이버 오픈 프로젝트: http://dev.naver.com/projects
.. _`https://github.com/{계졍명}/{저장소명}/wiki\*\*`: https://github.com/%7B계졍명%7D/%7B저장소명%7D/wiki**

.. |위키 만들기| image:: https://oss.navercorp.com/communication-service/open-project-migration/wiki/위키만들기.png
