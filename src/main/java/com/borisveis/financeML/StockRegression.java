package com.borisveis.financeML;

import yahoofinance.Stock;
import yahoofinance.YahooFinance;
import yahoofinance.histquotes.HistoricalQuote;
import yahoofinance.histquotes.Interval;
import tech.tablesaw.api.*;
import smile.regression.OLS;
import smile.validation.metric.MSE;
import smile.validation.metric.RSquared;

import org.knowm.xchart.*;
import org.knowm.xchart.style.Styler;

import java.io.IOException;
import java.time.LocalDate;
import java.time.ZoneId;
import java.util.*;
import java.util.stream.Collectors;

public class StockRegression {
    public static void main(String[] args) throws IOException {
        // Fetch data
        Table data = fetchData();

        // Prepare features and labels
        DoubleColumn aapl = data.doubleColumn("AAPL");
        DoubleColumn spy = data.doubleColumn("SPY");

        int size = data.rowCount();
        int splitIndex = (int) (size * 0.8);

        // Convert the data into double[][] for features and double[] for labels
        double[] aaplArray = aapl.asDoubleArray();
        double[][] X = Arrays.stream(aaplArray)
                .mapToObj(d -> new double[]{d})
                .toArray(double[][]::new);

        double[] y = spy.asDoubleArray();

        // Split the data into training and test sets
        double[][] X_train = Arrays.copyOfRange(X, 0, splitIndex);
        double[][] X_test = Arrays.copyOfRange(X, splitIndex, size);
        double[] y_train = Arrays.copyOfRange(y, 0, splitIndex);
        double[] y_test = Arrays.copyOfRange(y, splitIndex, size);

        // Train model using OLS (Ordinary Least Squares)
        OLS model = OLS.fit(X_train, y_train);

        // Predict and evaluate the model
        double[] y_pred = new double[X_test.length];
        for (int i = 0; i < X_test.length; i++) {
            y_pred[i] = model.predict(X_test[i]);
        }

        double mse = MSE.of(y_test, y_pred);
        double r2 = RSquared.of(y_test, y_pred);

        System.out.printf("Mean Squared Error: %.4f%n", mse);
        System.out.printf("R-squared: %.4f%n", r2);

        // Plot the results
        plotResults(X_test, y_test, y_pred);
    }

    public static Table fetchData() throws IOException {
        Calendar from = Calendar.getInstance();
        from.add(Calendar.YEAR, -5);

        // Fetch historical stock data for AAPL and SPY
        Stock spyStock = YahooFinance.get("SPY");
        Stock aaplStock = YahooFinance.get("AAPL");

        List<HistoricalQuote> spyHist = spyStock.getHistory(from, Interval.DAILY);
        List<HistoricalQuote> aaplHist = aaplStock.getHistory(from, Interval.DAILY);

        List<Date> dates = new ArrayList<>();
        List<Double> spyClose = new ArrayList<>();
        List<Double> aaplClose = new ArrayList<>();

        for (int i = 0; i < Math.min(spyHist.size(), aaplHist.size()); i++) {
            HistoricalQuote s = spyHist.get(i);
            HistoricalQuote a = aaplHist.get(i);

            if (s.getClose() != null && a.getClose() != null) {
                dates.add(s.getDate().getTime());
                spyClose.add(s.getClose().doubleValue());
                aaplClose.add(a.getClose().doubleValue());
            }
        }

        return Table.create("Stock Data")
                .addColumns(
                        DateColumn.create("Date", dates),
                        DoubleColumn.create("SPY", spyClose),
                        DoubleColumn.create("AAPL", aaplClose)
                );
    }

    public static void plotResults(double[][] X_test, double[] y_test, double[] y_pred) {
        // Scatter Plot
        XYChart scatter = new XYChartBuilder().width(600).height(400).title("Actual vs Predicted SPY").xAxisTitle("Actual").yAxisTitle("Predicted").build();
        scatter.getStyler().setLegendPosition(Styler.LegendPosition.InsideSE);

        scatter.addSeries("Predicted vs Actual", y_test, y_pred);

        // Time Series Plot
        double[] xvals = Arrays.stream(X_test).mapToDouble(x -> x[0]).toArray();

        XYChart timeSeries = new XYChartBuilder().width(600).height(400).title("AAPL vs SPY").xAxisTitle("AAPL").yAxisTitle("SPY").build();
        timeSeries.addSeries("Actual SPY", xvals, y_test);
        timeSeries.addSeries("Predicted SPY", xvals, y_pred);

        // Show Charts
        new SwingWrapper<>(List.of(scatter, timeSeries)).displayChartMatrix();
    }
}
