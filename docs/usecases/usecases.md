In this section we try to explain some normal usecases for __Piri__.

It is highly recommended that you go through the [introduction](../../introduction) before continuing

## Piri + CSV

CSV is one of the most used filetypes when exchanging data by files. Here are some examples to look at when working with csv

* [Transform CSV data to JSON](../csv_to_json)
* [Transform JSON to CSV]()
* [Row Type CSV data]()


## Piri + XML

XML is... ugh... but a lot of legacy systems expect XML as input and produces XML as output. We won't get rid of XML anytime soon, but atleast with piri we can live with it.

There are three things to look out for when working with XML.

1. __It's impossible to know if a child of an element is supposed to be an array or not.__
2. __XML creates structure with Elements, but store data as either parameters or as text between element opening and closing tag.__

Because of this there are no 1 to 1 XML->JSON converter that will work for any XML. Conventions  must be chosen but a good starting point is the Parker convention

* [Restructure XML data with Piri]()
* [From XML to CSV]()
* [CSV to XML]()

## Other usecases

Add an issue at our [issue tracker](https://github.com/greenbird/piri/issues) for request for other usecases/examples
