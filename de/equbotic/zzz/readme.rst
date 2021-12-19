  /*
.. */
  package de.kfw.kr.rmp_kupf.kfktCluster.Allgemeine_Funktionen
  import  de.kfw.kr.rmp_kupf.common.typenverzeichnis.T._
  import  de.kfw.kr.rmp_kupf.common.parametrisierung.P._
  import  de.kfw.kr.rmp_kupf.common.overrides.O._
  import  de.kfw.kr.rmp_kupf.common.funktionen.F._
  import  de.kfw.kr.rmp_kupf.gomSichten.Risikopositionen._
  import  de.kfw.kr.rmp_kupf.gomSichten.Geschaefte._
  import  de.kfw.kr.rmp_kupf.gomSichten.Geschaeftspartner._
  import  de.kfw.kr.rmp_kupf.gomSichten.Ratings._
  import  de.kfw.kr.rmp_kupf.gomSichten.Sicherheiten._
  import  de.kfw.kr.rmp_kupf.gomSichten.Ergebnisse._
  import  de.kfw.kr.rmp_kupf.kalkProzess.Kontext
  /*
.. contents::
   :depth: 3
   :local:

##########################
Bewertungsansatz bestimmen 
##########################

Fachlicher Kontext
==================
Fachliche Beschreibung der Funktion
-----------------------------------
Die Kalkulationsfunktion Bewertungsansatz bestimmen spezifiziert die Berechnungslogik zur Bestimmung des Bewertungsansatzes für Risikopositionen ohne Berücksichtigung der Besicherungsstruktur und auf Ebene der Assoziation (Teilexposure->Sicherheit) unter Berücksichtigung der Besicherung.

Im Anwendungsfall zur Bestimmung des regulatorischen Kapitals gibt der Bewertungsansatz an, ob eine Risikoposition bzw. eine Assoziation (Teilexposure->Sicherheit) gemäß dem KSA oder IRBA zu bewerten ist. Die Berechnungslogik berücksichtigt dabei die Anforderungen der CRR [1] und setzt die durch die KfW wahrgenommenen Wahlmöglichkeiten um (vgl. Fachinformation [2]).

.. math::

         (a + b)^2 = a^2 + 2ab + b^2

         (a - b)^2 = a^2 - 2ab + b^2

In Bezug auf die regulatorische Bewertung sind dabei folgende Ausprägungen des Bewertungsansatzes zu differenzieren[1]:
 
 .. math::

         (a + b)^2  &=  (a + b)(a + b) \\
                    &=  a^2 + 2ab + b^2 
 
-      <CCP>: Handelsrisikopositionen gegenüber zentralen Gegenparteien (inkl. Beiträge zum Ausfallfonds der zentralen Gegenpartei(en)) werden auf Grundlage eines eigenständigen Bewertungsansatzes entsprechend Teil 3, Titel II, Kapitel 6, Abschnitt 9 der CRR behandelt (CRR Artikel 107 (2), Satz 1 und [3]).
-      <IRBA>: Bewertung gemäß IRBA, da für die entsprechenden Elemente geeignete und von der zuständigen Aufsicht zugelassene Ratingverfahren existieren.
-      <KSA − Übergangsbestimmungen>: Vorübergehende Anwendung des KSA ohne Anrechnung auf den Abdeckungsgrad, z.B. aktuell noch für Risikopositionen aus Beteiligungen gemäß CRR Artikel 495 (1)[2].
-      <KSA − Dauerhafter Ausnahmetatbestand>: Dauerhafte Anwendung des KSA ohne Anrechnung auf den Abdeckungsgrad (Ausnahmetatbestand gemäß CRR Artikel 150), z.B. ansatzübergreifende Besicherung.
-      <KSA − Temporärer Partial Use>: Vorübergehende Anwendung des KSA mit Anrechnung auf den Abdeckungsgrad. Dieser Bewertungsansatz wird zugewiesen, wenn für die entsprechenden Positionen die Einführung entsprechender IRBA-Ratingverfahren mittelbar geplant ist.
-      <KSA − Dauerhafter Partial Use>: Dauerhafte Anwendung des KSA mit Anrechnung auf den Abdeckungsgrad. Dieser Bewertungsansatz wird zugewiesen, wenn unter Kosten/Nutzen Aspekten eine Einführung von IRBA-konformen Ratingverfahren angesichts einer geringen Anzahl an Positionen im Portfolio unverhältnismäßig aufwändig ist (vgl. auch CRR Artikel 150 (1), lit. c). Hierunter fallen beispielsweise Geschäfte der Mandanten DEG und TBG.

Die Berechnungslogik zur Bestimmung des Bewertungsansatzes orientiert sich im Wesentlichen an den Vorgaben der Fachinformation [2]. Dabei werden folgende Fälle in der aufgeführten Reihenfolge abgearbeitet:

-      CCP: Die Ausprägung <CCP> wird für die relevanten Geschäfte ungeachtet der folgenden Berechnungsvorschriften als Bewertungsansatz gesetzt.
-      Override: In einigen Fällen kann kein fachlich korrekter Bewertungsansatz automatisiert bestimmt werden. In diesen Fällen muss die Zuweisung per manuellem Override erfolgen. In welchen Fällen die Override-Funktionalität für den Bewertungsansatz zu verwenden ist, wird in der Fachinformation [2] festgelegt. Insbesondere sind das folgende Ausnahmetatbestände (vgl. CRR Artikel 150):
*       Ausnahmetatbestand für Verwaltungseinrichtungen, die ausschließlich der Bundesrepublik Deutschland, ihren Ländern oder Gemeinden oder Gemeindeverbänden unterstehen und deren Aufgaben wahrnehmen und die wie Institute behandelt werden.
*       Ausnahmetatbestand für kommunal verbürgtes Inlandsgeschäft (auslaufender Geschäftsbereich).
-      Mandanten im KSA: Für Risikopositionen der Mandanten, die vollständig im KSA geführt werden (aktuell die DEG und TBG), wird der Bewertungsansatz entsprechend gesetzt.
-      Geschäftsspezifische Zuordnung: Beteiligungen werden generell im IRBA bewertet und Verbriefungen einzelfallbasiert durch den Marktbereich auf Basis vorgegebener Kriterien dem IRBA bzw. KSA zugeordnet werden. Der Bewertungsansatz für Verbriefungen wird somit auf Geschäftsebene von außen vorgegeben und in dieser Kalkulationsfunktion für entsprechende Risikopositionen ohne weitere Prüfung übernommen.
-      Risikopositionen aus sonstigen Aktiva ohne Kreditverpflichtungen werden im IRBA geführt (siehe CRR Artikel 147 (2), lit. g, CRR Artikel 147 (9) i.V.m. CRR Artikel 148 (5)).
-      Risikopositionen, für die kein internes Rating vorliegt bzw. deren Risikoträger nicht eindeutig identifiziert werden kann (z.B. Sammelposten), können nicht gemäß IRBA bewertet werden und sind demnach dem Bewertungsansatz KSA zuzuordnen.
-      Geschäftspartnerspezifische Zuordnung zur Behandlung von Ausnahmetatbeständen und der Vererbung von Länderratings: Hier werden weitere Bestimmung des CRR Artikels 150 geprüft, für die eine automatisierte Zuordnung des Bewertungsansatzes möglich ist. Dies ist insbesondere der Fall für die Überprüfung der Vorgaben aus CRR Artikel 150 (1), lit. d. Auch werden in diesem Rahmen Risikopositionen von Geschäftspartnern deren Hauptgeschäftspartner staatliche Adressen darstellen betrachtet. Diese erben das Rating des entsprechenden Sitzlandes und werden generell, sofern kein dauerhafter Ausnahmetatbestand vorliegt, im IRBA bewertet.
-      Mengengeschäft (Retail): Risikopositionen von Geschäftspartnern aus dem Retail-Segment werden mandantenabhängig entweder im IRBA (KfW) oder im dauerhaften Partial Use (IPEX, DEG und TBG) geführt.
-      Standardableitung gemäß Mandant, Ratingverfahren und Ratingcluster: In allen anderen Fällen erfolgt die Zuordnung auf Basis der durch die Fachinformation [2] vorgegeben Zuordnung. Dabei erfolgt die Bestimmung des Bewertungsansatzes im Wesentlichen auf Basis des Ratingverfahrens sowie des Ratingclusters des unterlegungsrelevanten Ratings. Zusätzlich wird der Mandant des zugehörigen Geschäfts bzw. Netting-Kreises berücksichtigt.

Für den Fall, dass gemäß der beschriebenen Logik kein Bewertungsansatz abgeleitet werden konnte, wird der Bewertungsansatz auf <KSA − Dauerhafter Partial Use> gesetzt. Damit erfolgt die Bewertung dieser Risikopositionen generell gemäß dem Standardansatz. Das Auftreten dieses Falles wird für den fachlichen Betrieb durch das Setzen eines Prüfkennzeichens vermerkt.

Verwendete Formelzeichen und Abkürzungen
----------------------------------------
==============  ============
Zeichen         Beschreibung
==============  ============
BW_Kennzeichen  Vorläufiges Bewertungskennzeichen an der Risikoposition bzw. an der Assoziation
==============  ============

Modellreferenz
--------------
keine

Wichtige Basis für die Ableitung des Bewertungsansatzes ist die gegenwärtige fachliche Logik zur Bestimmung des Kennzeichens (siehe [2]).

Einbettung in Kreditrisikoarchitektur
-------------------------------------
Anwendungsbereich
.................
Die Kalkulationsfunktion wird in den folgenden Kalkulationsprozessen verwendet:

=================================================================  ========  ==================
Bezeichnung                                                        Referenz  Beschreibung 
=================================================================  ========  ==================
Risikokennzahlen für regulatorisches Kapital gemäß KSA berechnen   [4]       Fachliche Spezifikation der detaillierten Ablauflogik der Berechnung der Risikokennzahlen zur Bestimmung des regulatorischen Kapitalbedarfs gemäß KSA.  
Risikokennzahlen für regulatorisches Kapital gemäß IRBA berechnen  [5]       Fachliche Spezifikation der detaillierten Ablauflogik der Berechnung der Risikokennzahlen zur Bestimmung des regulatorischen Kapitalbedarfs gemäß IRBA.
=================================================================  ========  ==================

Vorbedingungen
..............
=================================================================  ========  ==================
Bezeichnung                                                        Referenz  Beschreibung 
=================================================================  ========  ==================
Designprinzipien und Notationsstandards                            [6]       Die im formalen Teil des Architekturrahmenwerks der Domäne Kreditrisiko aufgeführten Designprinzipien und Notationsstandards sind bei der Modellierung des Geschäftsobjektclusters zu berücksichtigen
=================================================================  ========  ==================

Formale Kalkulationsfunktionsbeschreibung
=========================================
Definition
----------
Name
....
Bewertungsansatz bestimmen

Definition
..........
Die Kalkulationsfunktion bestimmt den Bewertungsansatz auf Basis von Eigenschaften der übergebenen Risikoposition oder der Assoziation (Teilexposure‑>Sicherheit) und des zu betrachtenden Geschäftspartners.
 
Anmerkung
.........
Im Falle eines Ausfalls bleibt das Ratingverfahren bestehen, nur die Rating-Klasse wird auf M19 oder M20 umgesetzt. Deshalb kann im Allgemeinen auch für ausgefallene Geschäftspartner die Ermittlung gemäß der unten aufgeführten Berechnungslogik erfolgen. Liegt bei Ausfall kein Rating vor, wird ein Ausfallrating angelegt, welches gemäß Zuordnung aus [2] auf den Bewertungsansatz <KSA − Dauerhafter Partial Use> abgebildet wird. Meist kommt es zur Anwendung eines Ausfallratings für Retail-Geschäftspartner. In der untenstehenden Logik werden diese jedoch separat mit dem Bewertungsansatz <IRBA> versehen.

Zu beachten ist, dass Risikopositionen ohne (gültiges) internes Rating im KSA zu bewerten sind, weshalb für diese Positionen im Rahmen der generellen Vorgehensweise eine explizite Zuschlüsselung zum Bewertungsansatz <KSA> erfolgt. Kann gemäß der beschriebenen Logik kein Bewertungsansatz abgeleitet werden, so wird der Bewertungsansatz auf <KSA − Dauerhafter Partial Use> gesetzt.

Input
..... 
=========  =======================================  ============
Name       Typ                                      Beschreibung                                                    
=========  =======================================  ============
GO_Input   Geschäftsobjekt: Risikoposition          Ebene auf der der Bewertungsansatz bestimmt werden soll.
           oder
           Assoziation: (Teilexposure->Sicherheit)
GP_Input   Geschäftsobjekt:Geschäftspartner         Relevanter Geschäftspartner zur Ableitung des Bewertungsansatzes. Auf Risikopositionsebene ist dies immer der Risikoträger. Auf Ebene der Assoziation (Teilexposure->Sicherheit) ist dies der relevante Sicherheitengeber, der der Sicherheitengeber, ein Drittinstitut, ein Lebensversicherer oder ein Wertpapieremittent sein kann.
=========  =======================================  ============

Output
......
Die Ablage der Ergebnisse (= GO_Input_Ergebnisse) erfolgt entweder direkt an der übergebenen Risikoposition oder im Container Kennzahlen_SI der übergebenen Assoziation (Teilexposure‑>Sicherheit).

=================================================  ==================================  ============
Name                                               Typ                                 Beschreibung                                                    
=================================================  ==================================  ============
GO_Input_Ergebnisse. Bewertungsansatz              Aufzählungstyp: Bewertungsansatz    Je nachdem welches Element übergeben wurde, ist das Ergebnis der Kalkulationsfunktion der Bewertungsansatz auf Ebene der Risikoposition oder an der Assoziation (Teilexposure->Sicherheit).
GO_Input_Ergebnisse.FB_Bewertungsansatz_Fallback   Bool                                Kennzeichen für den fachlichen Betrieb.
                                                                                       Je nachdem welches Element übergeben wurde, markiert das Kennzeichen die Setzung eines Fallback-Bewertungsansatzes auf Ebene der Risikoposition oder an der Assoziation (Teilexposure->Sicherheit).
=================================================  ==================================  ============

     
Benötigte variable Attribute
............................
=================================================  ==================================  ============
Name                                               Typ                                 Beschreibung                                                    
=================================================  ==================================  ============
GO_Input_Ergebnisse.Rating_relevant                Aufzählungstyp: Bewertungsansatz    Unterlegungsrelevantes Rating zur PD-Bestimmung
=================================================  ==================================  ============

variable Parameter
.................. 
=================================================  ==================================  ============
Name                                               Typ                                 Beschreibung                                                    
=================================================  ==================================  ============
CRR_Bewertungsansatz                               Aufzählungstyp: Bewertungsansatz    Parametersatz: Steuerung_Bewertungsansätze. Zugriff über Ratingverfahren, Ratingcluster und Mandant.
CRR_Bewertungsansatz_GP                            Aufzählungstyp: Bewertungsansatz    Parametersatz: Steuerung_Bewertungsansätze. Zugriff über Sitzland.   
=================================================  ==================================  ============

Berechnungslogik
----------------

Die eigentliche Ableitung des Bewertungsansatzes erfolgt anhand der folgenden Schritte:
1.    CCP
2.    Override,
3.    Mandanten im KSA,
4.    Geschäftsspezifische Zuordnung von Beteiligungen und Verbriefungen,
5.    Positionen aus sonstigen Aktiva ohne Kreditverpflichtungen,
6.    Positionen ohne internes Rating bzw. ohne Risikoträger
7.    Geschäftspartnerspezifische Ausnahmetatbestände (gemäß CRR Artikel 150) und Vererbung von Länderratings,
8.    Mengengeschäft (Retail) und 
9.    Standardableitung gemäß Mandant, Ratingverfahren und Ratingcluster.

Kann gemäß dieser einzelnen Schritte kein Bewertungsansatz abgeleitet werden, so wird der Bewertungsansatz auf <KSA − Dauerhafter Partial Use> gesetzt.
Da der für die Risikoposition bzw. die Assoziation (Teilexposure->Sicherheit) relevante Mandant im Folgenden mehrfach verwendet wird, wird dieser in der lokalen Variable Mandant festgehalten. Der Mandant muss für Risikopositionen aus Netting-Kreisen über den Netting-Kreis bestimmt werden, anderenfalls über das Geschäft. Dies ist unabhängig von der Ebene, d.h. Risikoposition oder Assoziation (Teilexposure->Sicherheit):

.. code-block :: scala
 
  */
  object Bewertungsansatz_bestimmen {

    //[0]
    def apply (in: Risikoposition, Rating_relevant :Rating_intern_ib, out: Bew_Ansatz) 
    {
         apply_any(WAHR, in.Geschaeft, in.Geschaeft.Netting_Kreis,  
                   in.Risikotraeger, Rating_relevant, out)
    }
    
    def apply (sigeber: Geschaeftspartner_ib, rp :Risikoposition_ib, out: Bew_Ansatz) 
    {
        apply_any(FALSCH, 
                  rp.Geschaeft, rp.Geschaeft.Netting_Kreis,
                  sigeber,
                  sigeber.work_relevantes_Rating_GP, 
                  out)
    }
    
    //---------------------------------------------------------------------------------
    //---------------------------------------------------------------------------------
    def apply_any (isRisikoposition :Bool,  
                   Geschaeft   :Geschaeft_ib, Netting_Kreis :Netting_Kreis,
                   GP_Input    :Geschaeftspartner_ib, Rating_relevant :Rating_intern_ib,  
                   GO_Ergebnis :Bew_Ansatz) =
    {
      //Darauf aufbauend wird der Bewertungsansatz wie folgt bestimmt:
      val Mandant = NVL(Netting_Kreis.Mandant, Geschaeft.Mandant)
      
      val BW_Kennzeichen :Bewertungsansatz = { 
        
        //[1]  CCP
        if (    isRisikoposition == WAHR // GO_Input_any.isInstanceOf[Risikoposition]
            &&  GP_Input.CCP == WAHR 
            && (   (Geschaeft.OBJEKTTYP_  == OBJ_GE_HANDELSGESCHAEFT && Geschaeft.Handelsgeschaeft.Triparty_Repo == FALSCH )
                || (Netting_Kreis.Typ    .in (NK_DERIVATE, NK_REPO)  && Netting_Kreis.anzahlTripartyRepo > 0) 
               )
           )
            CCP

        //[2] SEC-ERBA
        else
        if (   isRisikoposition == WAHR // GO_Input_any.isInstanceOf[Risikoposition]
            && Geschaeft.OBJEKTTYP_  == OBJ_GE_VERBRIEFUNG
           )
            SEC_ERBA
            
        //[3]  Override
        else
        if (Override(OVR_BEWERTUNGSANSATZ, Geschaeft.Geschaeft_Id, GP_Input.Gp_Id, Netting_Kreis.Nk_Id) != UNDEF)
            Override(OVR_BEWERTUNGSANSATZ, Geschaeft.Geschaeft_Id, GP_Input.Gp_Id, Netting_Kreis.Nk_Id)  
           
      // PRI-Test Anfang    
  //   else
  //      if (isRisikoposition == FALSCH // Nur auf TESI für Sicherheitengeber durchführen 
  //        && (GP_Input.Gp_Id.in(10781582,20441905,5778813,20363849,17632973,9836378,5231358,77820002,16927542) 
  //        || GP_Input.Gp_Id.in (16927580,15191067,24569731,15510811,15092084,11633179,881446,16199224,86423711) 
  //        || GP_Input.Gp_Id.in (20365700,94922985, 76421341,17072694,15113332,80621368,17824989,80619916,80324460)
  //        || GP_Input.Gp_Id.in (16925038,2452163,10766585,12717519,18940899,18183168,19365519,23332578,23001831)
  //        || GP_Input.Gp_Id.in (86467492,76421309,20427880,20427900,10766540,15113326,11916330,20886621,17834688)
  //        || GP_Input.Gp_Id.in (19060464,93757530,76421333,20716211,80621465,94587388,11645361,76421287,83120017)
  //        || GP_Input.Gp_Id.in (12928447,11872055,39034356,98160591,98195166,20175919,24795943)))
  //       {
  //          IRBA
  //       }
      // PRI-Test Ende            
        //[4]  Mandanten im KSA
        else
        if (Mandant.in(DEG, TBG))
            Parametrisierung(PARS_STEUERUNG_BEWERTUNGSANSAETZE, PARN_CRR_BEWERTUNGSANSATZ, 
                             Array(UNDEF, UNDEF, Mandant) )

        //[5]	Bewertung von Intragruppenforderungen im KSA 
        else
        if (   GP_Input.Gp_Id.in (ADR_KFW, ADR_IPEX, ADR_DEG, ADR_TBG)
            && Parametrisierung(PARS_STEUERUNG_BEWERTUNGSANSAETZE, PARN_GENEHMIGTE_INTRAGRUPPENFORDERUNG, 
                                Array(GP_Input.Gp_Id))  == WAHR
           )
            KSA_DAUERHAFTER_PARTIALUSE
                             
        //[6]  Geschäftsspezifische Zuordnung von Beteiligungen 
        else
        if (   isRisikoposition == WAHR // GO_Input_any.isInstanceOf[Risikoposition]
            && Geschaeft.OBJEKTTYP_  == OBJ_GE_BETEILIGUNG
           )
        	if (Kontext.calc_Basel4)  KSA_UEBERGANGSBESTIMMUNG   //BASEL_IV: statt IRBA
        	else                      IRBA
        
        //ist oben bei -> 2 :: [4b]  Geschäftsspezifische Zuordnung von Verbriefungen  
  //      else
  //      if (   GO_Input_any.isInstanceOf[Risikoposition]
  //          && Geschaeft.OBJEKTTYP_  == OBJ_GE_VERBRIEFUNG
  //         )
  //          Geschaeft.Verbriefung.Bewertungsansatz   //CHECK fachsepz (war falsch)

        //[7] Positionen aus sonstigen Aktiva ohne Kreditverpflichtungen:
        else                                                          //CHECK fachspez falsch
        if (   isRisikoposition == WAHR // GO_Input_any.isInstanceOf[Risikoposition] 
            && Geschaeft.Geschaeft_sonstiges.Untertyp.
                               in ( KASSENBESTAND, GOLDBESTAND, SACHANLAGE,  
                                    LEASING, RECHNUNGSABGRENZUNGSPOSTEN,  
                                    IM_EINZUG_BEFINDLICHE_KASSENPOSITION ) 
           )
            IRBA

        //[8] Positionen ohne internes Rating bzw. ohne Risikoträger
        else                                                           
        if (   (   Rating_relevant.Rating_Id <= 0 )  //= rating undefined
            || (   isRisikoposition == WAHR // GO_Input_any.isInstanceOf[Risikoposition] 
                && Geschaeft.Geschaeft_sonstiges.Untertyp == SONSTIGE_RISIKOTRAEGER_NICHT_ZUORDENBAR )
           )
            KSA_DAUERHAFTER_PARTIALUSE
            
        //[9]  Geschäftspartnerspezifische Ausnahmetatbestände (gemäß CRR Artikel 150) und Vererbung von Länderratings
        else
        if (GP_Input.Behandlung_KSA in (ZENTRALSTAATEN_UND_ZENTRALBANKEN, WIE_ZENTRALSTAATEN_UND_ZENTRALBANKEN))
            Parametrisierung(PARS_STEUERUNG_BEWERTUNGSANSAETZE, PARN_CRR_BEWERTUNGSANSATZ_GP, 
                             Array(GP_Input.Sitzland_Id_op) )

        //[10]  Mengengeschäft (Retail)
        else
        if (GP_Input.Retail_op == WAHR && isRisikoposition == WAHR) //TODO CHECK Problem Retail_Op bei Sicherheitengeber ohne Geschaeft und Retaileinstufung
        {
           val retailsegmentgruppe    = Geschaeft.Retailsegmentgruppe
           val antragsratingverfahren = Rating_relevant.Antragsratingverfahren
           val parameter              = Parametrisierung(PARS_STEUERUNG_BEWERTUNGSANSAETZE, PARN_CRR_BEWERTUNGSANSATZ_RETAIL, 
                                                         Array(retailsegmentgruppe, antragsratingverfahren, Mandant) ) 
           if (parameter != UNDEF)
               parameter
           else
               KSA_DAUERHAFTER_PARTIALUSE
        }

        //[9]  Standardableitung gemäß Mandant, Ratingverfahren und Ratingcluster                             
        else 
        {
          //1.Ratingverfahren: Hauptdimension, die für jedes Rating gesetzt ist.
          val Ratingverfahren = Rating_relevant.Verfahren
          //2.Ratingcluster: [9b]
          val Ratingcluster   = Rating_relevant.Cluster
          //Die Ermittlung des Bewertungsansatzes folgt auf Basis 
          //dieser auf den Dimensionen aus der entsprechenden Parametrisierung.
          Parametrisierung(PARS_STEUERUNG_BEWERTUNGSANSAETZE, PARN_CRR_BEWERTUNGSANSATZ, 
                           Array(Ratingverfahren ,Ratingcluster, Mandant) ) 
        }
      }
       //ist eine Operation (Geschaef0t->Risikipos) und wird hier abgebildet   
      val Bewertungsansatz_grob = BW_Kennzeichen match {
                                        case CCP      => GROB_CCP
                                        case IRBA     => GROB_IRBA
                                        case SEC_ERBA => GROB_SEC_ERBA
                                        case _        => GROB_KSA
                                   }
      //[10]
      if (BW_Kennzeichen == UNDEF)
      {   
          GO_Ergebnis.Bewertungsansatz             = KSA_DAUERHAFTER_PARTIALUSE
          GO_Ergebnis.Bewertungsansatz_grob        = GROB_KSA
          GO_Ergebnis.Bewertungsansatz_Fallback = WAHR
      }
      else
      {
          GO_Ergebnis.Bewertungsansatz             = BW_Kennzeichen
          GO_Ergebnis.Bewertungsansatz_grob        = Bewertungsansatz_grob
          GO_Ergebnis.Bewertungsansatz_Fallback = FALSCH
      }
      GO_Ergebnis
    }    
  }

  /*

.. [0]  Die Risikoposition dient als Ausgangspunkt der Beschreibung von Navigationen innerhalb der Berechnungslogik. Sie wird deshalb in der Variable RP_Ausgangspunkt festgehalten. Ist das übergebene Objekt die Assoziation (Teilexposure->Sicherheit), muss zunächst auf die Risikopositionsebene navigiert werden. Diese Navigation ist trivial, da jedes Teilexposure nur mit genau einer Risikoposition verbunden sein kann. Die Variable RP_Ausgangspunkt wird demgemäß wie folgt definiert:
        Die Ablage der Kennzahlen und auch der Zugriff auf das Ergebnis hängt davon ab, auf welcher Ebene man sich befindet. Auf Risikopositionsebene erfolgt die Ablage an der Risikoposition selbst, während bei Berechnungen auf Ebene der Assoziation (Teilexposure->Sicherheit) die Ablage und der Zugriff über den Container (Teilexposure->Sicherheit).Kennzahlen_SI erfolgt.

.. [1]  Fachliche Anmerkung: Handelsrisikopositionen gegenüber qualifizierten zentralen Gegenparteien werden anhand eines eigenständigen, von KSA und IRBA separaten, Ansatzes bewertet (CRR Artikel 107 (2), Satz 1 i.V.m. CRR Artikel 301 (2) und Artikel 306 (1); vgl. auch [3]). Dieses Kennzeichen wird lediglich auf Risikopositionsebene gesetzt, da die Konstellation, dass eine qualifizierte CCP eine zentral geclearte Handelsposition durch eine persönliche Sicherheit absichert (vgl. auch CRR Artikel 201 (1), lit. h), in der Praxis unwahrscheinlich und das alternative Vorgehen (d.h. eine Behandlung als bilaterales Geschäft) als konservativ eingestuft werden kann.

.. [2]  Fachliche Anmerkung: Der gewählte Zugang überschreibt den Bewertungsansatz sowohl auf der Risikoposition als auch auf Ebene der Assoziation (Teilexposure‑>Sicherheit), wenn das hinter der Risikoposition oder dem Teilexposure befindliche eindeutige Geschäft oder der Netting-Kreis in Kombination mit dem übergebenen Geschäftspartner GP_Input zur Überschreibung vorgemerkt ist. Die NVL-Konstruktion überprüft, ob die Risikoposition aus einem Geschäft, oder einem Netting-Kreis gebildet worden ist. Da im Anwendungsfall KSA alle Risikopositionen gemäß KSA bewertet werden und dieser demnach den einzig relevanten Bewertungsansatz darstellt, ist die Override-Funktionalität nur in anderen Anwendungsfällen (insbesondere IRBA) relevant.
  
.. [3] Fachliche Anmerkung: Die Mandanten DEG und TBG werden aktuell vollständig im KSA geführt. Der gewählte Zugang erfolgt, da sonst in allen Sonderbehandlungen eine separate Behandlung dieser Mandanten erforderlich wäre. Erfolgt in diesem Bezug eine Anpassung des Bewertungsansatzes, so ist neben der Parametrisierung hier auch die Berechnungslogik dahingehend anzupassen, dass der Mandant nicht mehr in diesen Zweig ausgesteuert wird.

.. [4a] Fachliche Anmerkung: Perspektivisch werden alle Beteiligungen dem Bewertungsansatz IRBA zugeordnet. Die Ausnahme von Beteiligungen, die vor dem 01.01.2007 abgeschlossen worden sind und die noch bis zum 31.12.2017 gemäß Grandfathering in <KSA − Dauerhafter Partial Use> geführt werden können (siehe [5]), wird hier nicht mehr abgebildet, da die Methodik erst nach dem 01.01.2018 produktiv gestellt wird. Diese Zuordnung ist unabhängig vom Vorliegen eines internen Ratings, da die KfW zur Bewertung von Beteiligungen den einfachen Risikogewichtungsansatz gemäß CRR Artikel 155 (2) verwendet. 

.. [4b] Fachliche Anmerkung: Verbriefungen werden einzelfallbasiert durch den Marktbereich, plausibilisiert durch RCf1, auf Basis vorgegebener Kriterien dem IRBA bzw. KSA zugeordnet (siehe Anhang der Fachinformation [2]). Die Zuordnung wird angeliefert und hier entsprechend übernommen. Diese Zuordnung ist unabhängig vom Vorliegen eines internen Ratings, da die KfW zur Bewertung von Verbriefungen den rating-basierten Ansatz auf Grundlage von externen Bonitätsbeurteilungen gemäß CRR Artikel 261 verwendet.

.. [5] Fachliche Anmerkung: Gemäß CRR Artikel 148 (5) werden sonstige Aktiva ohne Kreditverpflichtungen (siehe CRR Artikel 148 (2) und (9)) im IRBA geführt.

.. [6] Fachliche Anmerkung: Positionen, für die kein internes Rating vorliegt (z.B. Risiken gegenüber Ländern) bzw. deren Risikoträger nicht eindeutig identifiziert werden kann (z.B. Sammelposten aus Mitarbeiterkrediten), können nicht gemäß IRBA bewertet werden und sind demnach dem Bewertungsansatz KSA zuzuordnen. 

.. [7] Fachliche Anmerkung: Relevante Geschäftspartner innerhalb der Europäischen Union, die zur Gruppe der Zentralstaaten oder Zentralbanken oder zu regionalen und lokalen Gebietskörperschaften, Verwaltungseinrichtungen oder öffentlichen Stellen gehören, die wie Staaten behandelt werden und gemäß CRR Artikel 114 (2) und (4) ein KSA Risikogewicht von 0% erhalten, können gemäß CRR Artikel 150 (1) lit. d im KSA geführt werden (Ausnahmetatbestand). Hier werden zunächst nur Adressen mit Sitzland Bundesrepublik Deutschland verwendet und damit eine konservativere Lösung umgesetzt (andere Adressen der Europäischen Union könnten prinzipiell auch gemäß Ausnahmetatbestand im KSA geführt werden). Aus diesem Grund ist eine Überprüfung (und damit eine vorgeschaltete Bestimmung) des KSA-Risikogewichts nicht notwendig, da entsprechenden Adressen mit Sitzland Bundesrepublik Deutschland immer ein Risikogewicht von 0% aufweisen. Da es sich allgemein um eine optionale Bedingung handelt, ist der dargestellte Ansatz so valide.
    
       In der Regel wird für die genannten Adressen kein separates Rating durchgeführt (in Ausnahmefällen kann es auch Ratings zur internen Steuerung geben, die aber nicht zum Bewertungsansatz IRBA führen sollen). Aus diesem Grund müssen die genannten Adressen hier separat behandelt werden und können nicht gemäß der Standardzuordnung über ihr Rating eingruppiert werden.
    
       Generell ist in Bezug auf die zuvor genannten Geschäftspartner eine vollständige automatisierte Identifikation in sämtlichen Fällen nicht möglich. Beispielsweise werden Verwaltungseinrichtungen, die ausschließlich der Bundesrepublik Deutschland, ihren Ländern oder Gemeinden oder Gemeindeverbänden unterstehen und deren Aufgaben wahrnehmen, wie Institute behandelt. Die Einordnung muss ggf. durch einen Override erfolgen. Da es sich bei den Ausnahmetatbeständen um eine Kann-Bestimmung handelt, ist die Umsetzung nicht zwingend (siehe für die beschriebene Ableitung auch [5]).
    
       Alle anderen Hauptgeschäftspartner, die staatliche Adressen darstellen, erben das Rating des entsprechenden Sitzlandes und werden gemäß [2] auf IRBA gesetzt, sofern kein dauerhafter Ausnahmetatbestand vorliegt. Die hier behandelten Fälle sind beispielsweise staatliche Geschäftspartner anderer Mitgliedsstaaten.
    
.. [8] Fachliche Anmerkung: Geschäftspartner aus dem Retail-Segment werden mandantenspezifisch im IRBA (KfW) oder dauerhaften Partial Use (IPEX, DEB, TBG) geführt. Um Positionen dieser Art korrekt einordnen zu können, erfolgt dieser Prüfschritt vor den ratingverfahrensabhängigen Prüfungen (vgl. auch [2]).

.. [9] In allen anderen Fällen erfolgt die Zuordnung auf Basis der Tabelle „Zuordnung Ratingverfahren zu Bewertungsansätzen“ in [2]. Die Ermittlung erfolgt im Wesentlichen auf Basis des Ratingverfahrens und des Ratingclusters des unterlegungsrelevanten Ratings (Rating_relevant). Zusätzlich wird der Mandant des zugehörigen Geschäfts bzw. Netting-Kreises berücksichtigt. Das Ratingverfahren und der Ratingcluster werden hierfür zusätzlich bestimmt und in den gleichnamigen lokalen Variablen festgehalten:

.. [9b] Nicht für jedes Verfahren wird der Ratingcluster als Feinstruktur vorgesehen. In der Zuordnungslogik der Parametrisierung wird daher das nicht-Vorliegen eines Ratingclusters explizit behandelt (vgl. [7]).[3]

.. [10] Ist gemäß der beschriebenen Logik keine Ableitung des Bewertungsansatzes möglich, so wird der Bewertungsansatz auf <KSA − Dauerhafter Partial Use> gesetzt. Das Auftreten dieses Falles wird in einem Prüfkennzeichen entsprechend vermerkt. 

  */
