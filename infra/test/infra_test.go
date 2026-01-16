package test

import (
	"testing"
	"github.com/gruntwork-io/terratest/modules/terraform" // This is the anchor
	"github.com/stretchr/testify/assert"
)

func TestDynamoDBTable(t *testing.T) {
	t.Parallel()

	terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		TerraformDir: "../", // Path to your main.tf
	})

	defer terraform.Destroy(t, terraformOptions)
	terraform.InitAndApply(t, terraformOptions)

	tableName := terraform.Output(t, terraformOptions, "table_name")
	assert.NotEmpty(t, tableName)
}