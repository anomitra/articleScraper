// qsvgrenderer.sip generated by MetaSIP on Thu Feb 26 12:17:06 2015
//
// This file is part of the QtSvg Python extension module.
//
// Copyright (c) 2015 Riverbank Computing Limited <info@riverbankcomputing.com>
// 
// This file is part of PyQt5.
// 
// This file may be used under the terms of the GNU General Public License
// version 3.0 as published by the Free Software Foundation and appearing in
// the file LICENSE included in the packaging of this file.  Please review the
// following information to ensure the GNU General Public License version 3.0
// requirements will be met: http://www.gnu.org/copyleft/gpl.html.
// 
// If you do not wish to use this file under the terms of the GPL version 3.0
// then you may purchase a commercial license.  For more information contact
// info@riverbankcomputing.com.
// 
// This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
// WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.


class QSvgRenderer : QObject
{
%TypeHeaderCode
#include <qsvgrenderer.h>
%End

%ConvertToSubClassCode
    static struct class_graph {
        const char *name;
        sipTypeDef **type;
        int yes, no;
    } graph[] = {
        {sipName_QSvgRenderer, &sipType_QSvgRenderer, -1, 1},
        {sipName_QSvgWidget, &sipType_QSvgWidget, -1, 2},
        {sipName_QGraphicsSvgItem, &sipType_QGraphicsSvgItem, -1, -1},
    };
    
    int i = 0;
    
    sipType = NULL;
    
    do
    {
        struct class_graph *cg = &graph[i];
    
        if (cg->name != NULL && sipCpp->inherits(cg->name))
        {
            sipType = *cg->type;
            i = cg->yes;
        }
        else
            i = cg->no;
    }
    while (i >= 0);
%End

public:
    QSvgRenderer(QObject *parent /TransferThis/ = 0);
    QSvgRenderer(const QString &filename, QObject *parent /TransferThis/ = 0);
    QSvgRenderer(const QByteArray &contents, QObject *parent /TransferThis/ = 0);
    QSvgRenderer(QXmlStreamReader *contents, QObject *parent /TransferThis/ = 0);
    virtual ~QSvgRenderer();
    bool isValid() const;
    QSize defaultSize() const;
    bool elementExists(const QString &id) const;
    QRect viewBox() const;
    QRectF viewBoxF() const;
    void setViewBox(const QRect &viewbox);
    void setViewBox(const QRectF &viewbox);
    bool animated() const;
    QRectF boundsOnElement(const QString &id) const;
    int framesPerSecond() const;
    void setFramesPerSecond(int num);
    int currentFrame() const;
    void setCurrentFrame(int);
    int animationDuration() const;

public slots:
    bool load(const QString &filename);
    bool load(const QByteArray &contents);
    bool load(QXmlStreamReader *contents);
    void render(QPainter *p);
    void render(QPainter *p, const QRectF &bounds);
    void render(QPainter *painter, const QString &elementId, const QRectF &bounds = QRectF());

signals:
    void repaintNeeded();
};
