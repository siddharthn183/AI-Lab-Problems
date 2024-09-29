
library(bnlearn)
library(caret)
library(e1071)

course_grades <- read.table("2020_bn_nb_data (1).txt", header = TRUE)

factor_columns <- c("EC100", "EC160", "IT101", "IT161", "MA101", "PH100", "PH160", "HS101", "QP")
course_grades[factor_columns] <- lapply(course_grades[factor_columns], factor)

grade_levels <- c("AA", "AB", "BB", "BC", "CC", "CD", "DD", "F")

bayes_net <- hc(course_grades, score = "k2")

fitted_bn <- bn.fit(bayes_net, course_grades)

max_prob <- 0.0
predicted_grade <- ""

for (grade in grade_levels) {
    prob <- cpquery(fitted_bn, event = (PH100 == grade),
                    evidence = (EC100 == "DD" & IT101 == "CC" & MA101 == "CD"))
    if (prob > max_prob) {
        max_prob <- prob
        predicted_grade <- grade
    }
}

cat("Predicted Grade for PH100:", predicted_grade, "\n")

set.seed(100)
train_idx <- createDataPartition(course_grades$QP, p = 0.7, list = FALSE)
train_data <- course_grades[train_idx, ]
test_data <- course_grades[-train_idx, ]

naive_bayes_model <- naiveBayes(QP ~ EC100 + EC160 + IT101 + IT161 + MA101 + PH100 + PH160, data = train_data)

evaluate_model <- function(model, train_set, test_set) {
    # Predictions for training set
    train_pred <- predict(model, newdata = train_set, type = "class")
    train_table <- table(train_set$QP, train_pred)

    test_pred <- predict(model, newdata = test_set, type = "class")
    test_table <- table(test_set$QP, test_pred)

    train_accuracy <- sum(diag(train_table)) / sum(train_table)
    test_accuracy <- sum(diag(test_table)) / sum(test_table)

    cat("Training Accuracy:", round(train_accuracy, 4), "\n")
    cat("Test Accuracy:", round(test_accuracy, 4), "\n")
}

evaluate_model(naive_bayes_model, train_data, test_data)

trained_bn <- bn.fit(hc(train_data, score = "k2"), train_data)

bn_predictions <- predict(trained_bn, node = "QP", data = test_data)

confusion_matrix <- table(test_data$QP, bn_predictions)
bn_accuracy <- sum(diag(confusion_matrix)) / sum(confusion_matrix)

cat("Bayesian Network Test Accuracy:", round(bn_accuracy, 4), "\n")
