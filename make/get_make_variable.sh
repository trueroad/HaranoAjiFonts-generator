#!/bin/sh

VARIABLE_NAME="$1"
BUILD_DIR="$2"

if [ "${BUILD_DIR}" == "" ]; then
    BUILD_DIR=$(basename $(pwd))
fi

case "${VARIABLE_NAME}" in
    FONT_LANG )
        case "${BUILD_DIR}" in
            *JP* | *Gothic-* | *Mincho-* )
                echo JP
                ;;
            *CN* )
                echo CN
                ;;
            *TW* )
                echo TW
                ;;
            *-KR | *GothicKR-* | *MinchoKR-* )
                echo KR
                ;;
            *K1* )
                echo K1
                ;;
            * )
                echo ERROR
                exit 1
                ;;
        esac
        ;;
    FONT_TYPE )
        case "${BUILD_DIR}" in
            *Gothic* | *Sans* )
                echo Sans
                ;;
            *Mincho* | *Serif* )
                echo Serif
                ;;
            * )
                echo ERROR
                exit 1
                ;;
        esac
        ;;
    FONT_WEIGHT )
        case "${BUILD_DIR}" in
            *ExtraLight* )
                echo ExtraLight
                ;;
            *Light* )
                echo Light
                ;;
            *Normal* )
                echo Normal
                ;;
            *Regular* )
                echo Regular
                ;;
            *Medium* )
                echo Medium
                ;;
            *SemiBold* )
                echo SemiBold
                ;;
            *Bold* )
                echo Bold
                ;;
            *Heavy* )
                echo Heavy
                ;;
            * )
                echo ERROR
                exit 1
                ;;
        esac
        ;;
    * )
        echo ERROR
        exit 1
        ;;
esac
