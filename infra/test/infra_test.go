package test

import (
	"os/exec"
	"testing"
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestDynamoDBTable(t *testing.T) {
	t.Parallel()

	// Configure Terraform options pointing to the parent 'infra' directory
	terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		TerraformDir: "../",
	})

	// 1. Cleanup at the end no matter what
	defer terraform.Destroy(t, terraformOptions)

	// 2. Deploy the infrastructure
	terraform.InitAndApply(t, terraformOptions)

	// 3. Sequential Sub-test: Predict and Record
	t.Run("PythonAgentMemoryIntegration", func(t *testing.T) {
		cmd := exec.Command("python3", "-c", "from agent.agent_memory import AgentMemory; AgentMemory().record_prediction('VOO', 123.45, 'IntegrationTest')")
		cmd.Dir = "../../"
		output, err := cmd.CombinedOutput()
		assert.NoError(t, err, "Python AgentMemory write failed: %s", string(output))
	})

	// 4. Sequential Sub-test: Reflect on the recorded data
	t.Run("PythonReflectorIntegration", func(t *testing.T) {
		cmd := exec.Command("python3", "-c", "from agent.reflector import Reflector; Reflector().run_reflection()")
		cmd.Dir = "../../"
		output, err := cmd.CombinedOutput()
		assert.NoError(t, err, "Python Reflector failed: %s", string(output))
	})

	// 5. Verify Terraform Output
	tableName := terraform.Output(t, terraformOptions, "table_name")
	assert.Equal(t, "AgentPerformance", tableName)
}